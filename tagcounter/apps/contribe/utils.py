import hashlib


def calculate_cache_key(view_instance, view_method,
                        request, args, kwargs):
    m = hashlib.md5()
    m.update(request.query_params.get('url').encode('utf-8'))
    return m.hexdigest()
