import os
import django

# ✅ Establecer configuración de Django ANTES de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hcm.settings')
django.setup()

# ✅ Ahora sí importa el modelo
from consultas.models import RegistroFamiliar

import csv
from datetime import datetime

def run():
    with open('consulta_hcm.csv', encoding='utf-8-sig') as archivo_csv:
        lector = csv.DictReader(archivo_csv, delimiter=';')

        for fila in lector:
            try:
                fecha_nac = datetime.strptime(fila['FECHA DE NACIMIENTO'], '%d/%m/%Y').date()
            except (ValueError, KeyError):
                fecha_nac = None

            try:
                edad = int(fila['EDAD'])
            except (ValueError, KeyError):
                edad = None

            RegistroFamiliar.objects.create(
                ci_titular=fila['C.I TITULAR'].strip()[:20],
                apellidos=fila['APELLIDOS'].strip(),
                nombres=fila['NOMBRES'].strip(),
                ci_beneficiario=fila['C.I BENEFICIARIO'].strip()[:20],
                parentesco=fila['PARENTESCO'].strip(),
                sexo=fila['SEXO'].strip(),
                fecha_nacimiento=fecha_nac,
                edad=edad,
                telefono=fila['TELEFONO'].strip()[:20],
                correo=fila['CORREO ELECTRONICO'].strip(),
                discapacidad=fila['DISCAPACIDAD'].strip(),
                custodia_legal=fila['INDICAR BAJO CUSTODIA LEGAL'].strip(),
            )

    print("✅ ¡Datos importados exitosamente!")

if __name__ == '__main__':
    run()
