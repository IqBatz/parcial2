from decimal import Decimal, InvalidOperation
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from django.views import View
from .models import Ordenes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class OrdenesView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            ordenes = list(Ordenes.objects.filter(id=id).values())
            if len(ordenes) > 0:
                orden = ordenes[0]
                datos = {'message': "SUCCESS", "Orden": orden}
            else:
                datos = {'message': 'ERROR, orden no encontrada...'}
        else:
            ordenes = list(Ordenes.objects.values())
            if len(ordenes) > 0:
                datos = {"message": "SUCCESS", "Ordenes": ordenes}
            else:
                datos = {'message': 'ERROR, no se encontraron órdenes...'}
        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        try:
            total = Decimal(jd['total'])
            Ordenes.objects.create(nombreCliente=jd['nombreCliente'], total=total)
            return JsonResponse({'message': 'SUCCESS'})
        except InvalidOperation:
            return JsonResponse({'message': 'ERROR en el servidor'}, status=500)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            total = Decimal(jd.get('total', 0))
            ordenes = list(Ordenes.objects.filter(id=id).values())
            if len(ordenes) > 0:
                orden = Ordenes.objects.get(id=id)
                orden.nombreCliente = jd['nombreCliente']
                orden.total = total
                orden.save()
                datos = {"message": "SUCCESS"}
            else:
                datos = {"message": "ERROR, no se encontró la orden"}
            return JsonResponse(datos)
        except InvalidOperation:
            return JsonResponse({'message': 'ERROR en el servidor'}, status=500)

    def delete(self, request, id):
        ordenes = list(Ordenes.objects.filter(id=id).values())
        if len(ordenes) > 0:
            Ordenes.objects.filter(id=id).delete()
            datos = {"message": "SUCCESS, se eliminó la orden"}
        else:
            datos = {"message": "ERROR, no se encontró la orden"}
        return JsonResponse(datos)