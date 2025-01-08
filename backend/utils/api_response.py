from rest_framework.response import Response

def api_response(data=None, error=None, status_code=200):
    if error:
        return Response({"error": str(error)}, status=status_code)
    return Response(data, status=status_code)
