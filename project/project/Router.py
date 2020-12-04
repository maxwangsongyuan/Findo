class Router:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'Test':
            return db == 'default'
        if app_label == 'StockInfo':
            return db == 'default'
        if app_label == 'FinancialProduct':
            return db == 'default'
        if app_label == 'StructuredFinancialInvestment':
            return db == 'default'
        if app_label == 'Users':
            return db == 'mongo'
        if app_label == 'UserClicks':
            return db == 'mongo'
        if app_label == 'UserSaves':
            return db == 'mongo'
        return None