from django.shortcuts import render
from .models import RegistroFamiliar
from django.template.loader import render_to_string
from django.http import JsonResponse

def consultar_cedula(request):
    cedula = request.POST.get('cedula', '').strip()
    error = None
    resultados = None

    if not cedula.isdigit():
        error = "La cédula solo debe contener números."
    elif len(cedula) > 14:
        error = "La cédula no debe superar los 14 dígitos."
    else:
        resultados = RegistroFamiliar.objects.filter(ci_titular=cedula)
        if not resultados.exists():
            error = "No se encontraron resultados para la cédula proporcionada."

    context = {
        'error': error,
        'resultados': resultados if resultados else None,
        'cedula': cedula,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('consulta/resultado_parcial.html', context)
        return JsonResponse({
            'success': error is None,
            'html': html,
            'error': error,
        })

    return render(request, 'consulta/consulta.html', context)
