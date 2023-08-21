from flask import jsonify


class HandlerContext:

    @staticmethod
    def success(data=None, message=None, status_code=200):
        if isinstance(data, list):
            data = [item.to_dict() if hasattr(item, 'to_dict')
                    else item for item in data]
        elif hasattr(data, 'to_dict'):
            data = data.to_dict()

        response = {
            'message': message if message else 'Success',
            'data': data
        }
        return jsonify(response), status_code
