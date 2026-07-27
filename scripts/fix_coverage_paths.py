#!/usr/bin/env python3
"""
Corrige un coverage.xml (formato Cobertura, generado por coverage.py con
`--cov=.` corriendo DENTRO de un subdirectorio del monorepo) para que
SonarCloud pueda ubicar los archivos correctamente:

1. El <source> que coverage.py escribe es la ruta ABSOLUTA del runner en
   el que se genero (ej. /home/runner/work/.../auth-service). El scanner
   de SonarCloud corre dentro de un contenedor Docker que monta el repo en
   /github/workspace, asi que esa ruta absoluta no existe ahi -> se quita.

2. Los atributos `filename` quedan relativos al subdirectorio del servicio
   (ej. "services/jwt_service.py"), pero sonar.sources los espera
   relativos a la raiz del repo (ej. "auth-service/services/jwt_service.py").
   Se les antepone el prefijo del servicio.

Uso: python fix_coverage_paths.py <coverage.xml> <prefijo_del_servicio>
"""
import sys
import xml.etree.ElementTree as ET


def main():
    report_path, prefix = sys.argv[1], sys.argv[2]

    tree = ET.parse(report_path)
    root = tree.getroot()

    for cls in root.iter("class"):
        old_filename = cls.get("filename")
        if old_filename and not old_filename.startswith(f"{prefix}/"):
            cls.set("filename", f"{prefix}/{old_filename}")

    sources = root.find("sources")
    if sources is not None:
        root.remove(sources)

    tree.write(report_path, xml_declaration=True, encoding="UTF-8")
    print(f"[fix-coverage] {report_path}: filenames prefijados con '{prefix}/', <sources> eliminado.")


if __name__ == "__main__":
    main()
