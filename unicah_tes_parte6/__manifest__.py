{
    "name": "UNICAH - Trabajo Educativo Social",
    "version": "1.0",
    "summary": "Gestión de actividades y horas de Trabajo Educativo Social",
    "description": """
        Módulo para registrar el Trabajo Educativo Social
        de los estudiantes de UNICAH y controlar las
        horas acumuladas en sus actividades.
    """,
    "author": "UNICAH",
    "category": "Education",
    "depends": [
        "tienda_unicah",
    ],
    "data": [
        "security/ir.access.csv",
        "views/tes_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
