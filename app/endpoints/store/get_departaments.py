from app import Departament
from flask_restful import Resource


class GetDepartament(Resource):
    def get(self):
        try:
            departament = Departament.query.all()
            return {'status': 'ok',
                    'departament': [dep.to_dict(rules=('-store_departaments',)) for dep in departament]}, 200
        except Exception as e:
            return {'status': 'fail',
                    'message': str(e)}, 400
