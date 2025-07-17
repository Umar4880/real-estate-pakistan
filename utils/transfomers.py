from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoded_dec={}
    
    def fit(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            X=pd.DataFrame(X)
        
        for col in X.columns:
            freq=X[col].value_counts(normalize=True).to_dict()
            self.encoded_dec[col]=freq

        return self
    
    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            X=pd.DataFrame(X)

        for col in X.columns:
            if col in self.encoded_dec:
                X[col]=X[col].map(self.encoded_dec[col]).fillna(0)  
            else:
                raise ValueError(f"The {col} no exist in input features")
        return X


class CustomImputer(BaseEstimator, TransformerMixin):
    def __init__(self, impute_type=True, impute_bed=True, impute_bath=True, impute_locations=True):
        self.impute_type = impute_type
        self.impute_bed = impute_bed
        self.impute_bath = impute_bath
        self.impute_locations = impute_locations

        self.type_mode_by_area = {}
        self.bed_medians = {}
        self.bath_medians = {}
        self.loc_modes = {}
        self.city_modes = {}
        self.province_modes = {}

    def fit(self, X, y=None):
        X = X.copy()
        
        if self.impute_type and 'type' in X.columns:
            self.type_mode_by_area = X.groupby('area(sqft)')['type'] \
                .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan).to_dict()

        if self.impute_bed and 'bedroom' in X.columns:
            self.bed_medians = X.groupby(['area(sqft)', 'bath'])['bedroom'].median().to_dict()
        
        if self.impute_bath and 'bath' in X.columns:
            self.bath_medians = X.groupby(['area(sqft)', 'bedroom'])['bath'].median().to_dict()

        if self.impute_locations:
            if 'location' in X.columns:
                self.loc_modes = {}
                self.loc_modes.update({
                    ('city_prov', key): val.mode().iloc[0]
                    for key, val in X.groupby(['location_city', 'location_province'])['location']
                    if not val.mode().empty
                })
                self.loc_modes.update({
                    ('city', key): val.mode().iloc[0]
                    for key, val in X.groupby('location_city')['location']
                    if not val.mode().empty
                })
                self.loc_modes.update({
                    ('prov', key): val.mode().iloc[0]
                    for key, val in X.groupby('location_province')['location']
                    if not val.mode().empty
                })
            
            if 'location_city' in X.columns:
                self.city_modes = {}
                self.city_modes.update({
                    ('loc_prov', key): val.mode().iloc[0]
                    for key, val in X.groupby(['location', 'location_province'])['location_city']
                    if not val.mode().empty
                })
                self.city_modes.update({
                    ('loc', key): val.mode().iloc[0]
                    for key, val in X.groupby('location')['location_city']
                    if not val.mode().empty
                })
                self.city_modes.update({
                    ('prov', key): val.mode().iloc[0]
                    for key, val in X.groupby('location_province')['location_city']
                    if not val.mode().empty
                })
            
            if 'location_province' in X.columns:
                self.province_modes = {}
                self.province_modes.update({
                    ('loc_city', key): val.mode().iloc[0]
                    for key, val in X.groupby(['location', 'location_city'])['location_province']
                    if not val.mode().empty
                })
                self.province_modes.update({
                    ('city', key): val.mode().iloc[0]
                    for key, val in X.groupby('location_city')['location_province']
                    if not val.mode().empty
                })
                self.province_modes.update({
                    ('loc', key): val.mode().iloc[0]
                    for key, val in X.groupby('location')['location_province']
                    if not val.mode().empty
                })

        return self

    def transform(self, X):
        X = X.copy()

        if self.impute_type and 'type' in X.columns and X['type'].isnull().sum() > 0:
            X['type'] = X.apply(
                lambda row: self.type_mode_by_area.get(row['area(sqft)'], row['type'])
                if pd.isnull(row['type']) else row['type'], axis=1)

        if self.impute_bed and 'bedroom' in X.columns and X['bedroom'].isnull().sum() > 0:
            X['bedroom'] = X.apply(
                lambda row: self.bed_medians.get((row['area(sqft)'], row['bath']), row['bedroom'])
                if pd.isnull(row['bedroom']) else row['bedroom'], axis=1)

        if self.impute_bath and 'bath' in X.columns and X['bath'].isnull().sum() > 0:
            X['bath'] = X.apply(
                lambda row: self.bath_medians.get((row['area(sqft)'], row['bedroom']), row['bath'])
                if pd.isnull(row['bath']) else row['bath'], axis=1)

        if self.impute_locations:
            if 'location' in X.columns and X['location'].isnull().sum() > 0:
                X['location'] = X.apply(lambda row: self._impute_location(row, 'location'), axis=1)
            if 'location_city' in X.columns and X['location_city'].isnull().sum() > 0:
                X['location_city'] = X.apply(lambda row: self._impute_location(row, 'location_city'), axis=1)
            if 'location_province' in X.columns and X['location_province'].isnull().sum() > 0:
                X['location_province'] = X.apply(lambda row: self._impute_location(row, 'location_province'), axis=1)


        return X


    def _impute_location(self, row, col):
        if col == 'location' and pd.isnull(row['location']):
            return self.loc_modes.get(('city_prov', (row['location_city'], row['location_province'])),
                   self.loc_modes.get(('city', row['location_city']),
                   self.loc_modes.get(('prov', row['location_province']), row['location'])))
        
        if col == 'location_city' and pd.isnull(row['location_city']):
            return self.city_modes.get(('loc_prov', (row['location'], row['location_province'])),
                   self.city_modes.get(('loc', row['location']),
                   self.city_modes.get(('prov', row['location_province']), row['location_city'])))
        
        if col == 'location_province' and pd.isnull(row['location_province']):
            return self.province_modes.get(('loc_city', (row['location'], row['location_city'])),
                   self.province_modes.get(('city', row['location_city']),
                   self.province_modes.get(('loc', row['location']), row['location_province'])))
        
        return row[col]


class CustomPaymentImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.monthly_group_medians = {}
        self.initial_group_medians = {}
        

    def fit(self, X, y=None):
        X = X.copy()
        
        # Round values for grouping
        X['initial_round'] = X['initial_amount(Lakhs)'].round(0)
        X['monthly_round'] = X['monthly_installment(Lakhs)'].round(0)
        
        # Store medians as dictionaries
        self.monthly_group_medians = (
            X.groupby('initial_round')['monthly_installment(Lakhs)']
            .median().to_dict()
        )
        self.initial_group_medians = (
            X.groupby('monthly_round')['initial_amount(Lakhs)']
            .median().to_dict()
        )
        return self

    def transform(self, X):
        X = X.copy()
        X['initial_round'] = X['initial_amount(Lakhs)'].round(0)
        X['monthly_round'] = X['monthly_installment(Lakhs)'].round(0)
        
        # Impute monthly_installment
        mask = X['monthly_installment(Lakhs)'].isna()
        X.loc[mask, 'monthly_installment(Lakhs)'] = (
            X.loc[mask, 'initial_round'].map(self.monthly_group_medians)
        )
        
        # Impute initial_amount
        mask = X['initial_amount(Lakhs)'].isna()
        X.loc[mask, 'initial_amount(Lakhs)'] = (
            X.loc[mask, 'monthly_round'].map(self.initial_group_medians)
        )
        # Drop helper cols
        return X.drop(columns=['initial_round', 'monthly_round'])


class FeatureGeneration(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()

        # Create existing features
        X['area_x_bedroom'] = X['area(sqft)'] * X['bedroom']
        X['bed_bath_ratio'] = X['bedroom'] / (X['bath'] + 1)
        X['total_payments'] = X['initial_amount(Lakhs)'] + (X['monthly_installment(Lakhs)'] * X['remaining_installments'])
        
        X.drop(columns=['remaining_installments'], inplace=True, errors='ignore')
        return X