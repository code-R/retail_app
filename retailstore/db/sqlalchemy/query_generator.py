class QueryGenerator:
    DataMapper = {
        'locations': 'location_id',
        'departments': 'department_id',
        'categories': 'category_id',
        'sub_categories': 'sub_category_id',
    }

    def __init__(self, orm_model, orm_session, **kwargs):
        self.orm_model = orm_model
        self.orm_session = orm_session
        self.kwargs = kwargs

    @property
    def model_query(self):
        return self.orm_session.query(self.orm_model)

    @property
    def conditions(self):
        conditions = []
        for model in self.orm_model.join_models:
            key = self.DataMapper[model.__tablename__]
            conditions.append(getattr(model, 'id') == self.kwargs[key])

        return conditions

    def resources_query(self):
        query = self.model_query

        for join_model in self.orm_model.join_models:
            query = query.join(join_model)

        return query.filter(*self.conditions)

    def resource_query(self):
        query = self.resources_query()

        return query.filter(
            self.orm_model.id == self.kwargs['id'])
