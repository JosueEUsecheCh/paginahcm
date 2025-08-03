import os
import django
import csv
from datetime import datetime

# ✅ Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hcm.settings')
django.setup()

# ✅ Importa tu modelo
from consultas.models import RegistroFamiliar

def run():
    print("🗑️ Borrando todos los registros anteriores...")
    RegistroFamiliar.objects.all().delete()

    print("📥 Cargando nuevos datos desde CSV...")

    registros_batch = []  # lista para acumular objetos
    batch_size = 500  # ✅ mete de 500 en 500

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

            registros_batch.append(RegistroFamiliar(
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
            ))

            # ✅ Si la lista llega a 500, insertamos en bloque
            if len(registros_batch) >= batch_size:
                RegistroFamiliar.objects.bulk_create(registros_batch)
                registros_batch.clear()

        # ✅ Insertar lo que quedó pendiente
        if registros_batch:
            RegistroFamiliar.objects.bulk_create(registros_batch)

    print("✅ ¡Datos importados exitosamente!")

if __name__ == '__main__':
    run()
