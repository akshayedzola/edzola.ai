#!/usr/bin/env python3
"""Build the Spanish and Brazilian Portuguese vertical landing pages."""

from html import escape
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUGS = {
    "hub": "",
    "programme": "programme-evidence-systems",
    "funding": "fundraising-donor-grant-systems",
    "people": "people-hr-systems",
    "finance": "finance-operations-systems",
    "procurement": "procurement-inventory-systems",
}

COMMON = {
    "es": {
        "html_lang": "es",
        "home": "/es/",
        "vertical_root": "/es/verticals/",
        "what": "Qué hacemos",
        "verticals": "Verticales",
        "all": "Todas las verticales",
        "programme": "Programas y evidencia",
        "funding": "Financiación y relaciones",
        "people": "Personas y RR. HH.",
        "finance": "Finanzas y operaciones",
        "procurement": "Compras e inventario",
        "sectors": "Sectores",
        "thinking": "Ideas",
        "about": "Nosotros",
        "talk": "Habla con nosotros",
        "menu": "Menú",
        "skip": "Saltar al contenido",
        "explore": "Explorar",
        "start": "Empezar",
        "transformation": "Parte de una transformación digital de toda la organización",
        "related": "Trabajo y recursos relacionados",
        "case": "Leer el caso ↗",
        "guide": "Abrir el recurso →",
        "country": "Coimbatore · India",
        "reference_note": "Los casos y guías completos permanecen en EdZola para mantener el detalle en un solo lugar.",
    },
    "pt": {
        "html_lang": "pt-BR",
        "home": "/pt/",
        "vertical_root": "/pt/verticals/",
        "what": "O que fazemos",
        "verticals": "Verticais",
        "all": "Todas as verticais",
        "programme": "Programas e evidências",
        "funding": "Captação e relacionamentos",
        "people": "Pessoas e RH",
        "finance": "Finanças e operações",
        "procurement": "Compras e estoque",
        "sectors": "Setores",
        "thinking": "Reflexões",
        "about": "Sobre",
        "talk": "Fale com a gente",
        "menu": "Menu",
        "skip": "Pular para o conteúdo",
        "explore": "Explorar",
        "start": "Começar",
        "transformation": "Parte de uma transformação digital em toda a organização",
        "related": "Trabalhos e recursos relacionados",
        "case": "Leia o caso ↗",
        "guide": "Abra o recurso →",
        "country": "Coimbatore · Índia",
        "reference_note": "Os casos e guias completos permanecem na EdZola para manter os detalhes em um só lugar.",
    },
}

PAGES = {
    "es": {
        "hub": {
            "title": "Sistemas para ONG: programas, financiación, RR. HH. y operaciones | EdZola",
            "description": "Sistemas conectados para programas, evidencia, captación, donantes, subvenciones, RR. HH., finanzas y operaciones, con transformación digital por etapas.",
            "eyebrow": "Sistemas por necesidad organizativa",
            "h1": "Tu misión es específica. Los sistemas que la sostienen se repiten.",
            "lead": "EdZola diseña los sistemas conectados que permiten a las organizaciones con propósito ejecutar programas, demostrar resultados, gestionar financiación, apoyar a sus equipos y coordinar el trabajo. Empieza por un flujo roto o transforma la organización en una secuencia deliberada.",
            "intro": "Cuatro pilares conectados",
            "intro_body": "Cada pilar puede funcionar solo, conectarse con lo que ya usas o convertirse en una etapa de una hoja de ruta para toda la organización.",
            "pillars": [
                ("programme", "01 · Programas y evidencia", "Sabe quién recibió qué, qué cambió y qué necesita atención.", "MIS de programas, casos, indicadores, seguimientos, tableros e informes alrededor de un registro útil."),
                ("funding", "02 · Financiación y relaciones", "Sigue el dinero y las relaciones desde la primera conversación hasta el informe final.", "CRM de captación, donantes, donaciones, subvenciones, presupuestos, tramos, utilización y renovaciones."),
                ("people", "03 · Personas y RR. HH.", "Da a cada persona empleada un recorrido fiable desde la contratación hasta la salida.", "Selección, expedientes, incorporación, permisos, asistencia, nómina, desempeño y gastos."),
                ("finance", "04 · Finanzas y operaciones", "Haz que presupuestos, aprobaciones, proyectos y ejecución avancen juntos.", "Control presupuestario, gastos, proyectos, tareas, documentos, campañas y traspasos contables."),
            ],
            "transform_title": "Transforma toda la organización sin un despliegue de golpe.",
            "transform_body": "Reducimos la tensión trazando cómo fluyen el trabajo, los datos y las decisiones entre los procesos y sistemas existentes. Después secuenciamos el cambio para que cada entrega reduzca presión antes de la siguiente.",
            "steps": ["Mapear el trabajo real", "Simplificar primero", "Estabilizar los registros básicos", "Conectar los traspasos", "Automatizar y aprender"],
            "cta_title": "¿Dónde se rompe hoy el trabajo?",
            "cta_body": "Trae el flujo, la hoja, el informe o el traspaso que genera más presión. Te ayudaremos a decidir si conviene reparar un sistema o planificar una transformación más amplia.",
            "cta_label": "Mapear el siguiente paso útil",
        },
        "programme": {
            "title": "MIS de programas, gestión de casos y sistemas de MEL | EdZola",
            "description": "Sistemas de programas, casos, seguimiento, evaluación e informes que conectan la ejecución en campo con decisiones fiables.",
            "eyebrow": "Sistemas de programas y evidencia",
            "h1": "Sabe quién recibió qué, qué cambió y qué necesita atención.",
            "lead": "Diseñamos MIS de programas, gestión de casos, seguimiento, evaluación e informes alrededor del recorrido real de participantes, aliados y equipos de campo.",
            "section_title": "El informe solo es tan fiable como el recorrido que hay debajo.",
            "section_body": "Los problemas suelen empezar antes: identidades duplicadas, etapas confusas, retrasos sin conexión, indicadores cambiantes o seguimientos fuera del sistema.",
            "cards": [("Recorridos fragmentados", "La misma persona aparece en varias hojas y nadie ve su historia completa."), ("Visibilidad tardía", "Los responsables descubren abandonos cuando el programa ya terminó."), ("Presión de informes", "Cada financiador recibe una versión reconstruida manualmente.")],
            "workflow": ["Diseño, resultados y metas", "Inscripción, consentimiento e identidad", "Servicios, asistencia y casos", "Evaluaciones, derivaciones e hitos", "Seguimiento, resultados y calidad", "Decisiones, aprendizaje e informes"],
            "modules_title": "Un sistema de trabajo para primera línea, no solo una base para informes.",
            "modules": [("Participantes y hogares", "Identidad, consentimiento, relaciones, elegibilidad, ubicación e historial."), ("Programas y servicios", "Cohortes, sesiones, asistencia, derechos, socios y actividades de campo."), ("Casos y derivaciones", "Necesidades, riesgos, planes, notas, documentos y seguimientos."), ("Experiencia de campo", "Formularios móviles, trabajo sin conexión, portales, validaciones y revisión.")],
            "transform_title": "Los datos de programa ganan valor cuando se encuentran con financiación, personas y finanzas.",
            "transform_body": "Estabilizamos primero el recorrido del participante y conectamos después informes a donantes, obligaciones, asignación de personal, gastos y decisiones.",
            "cta_title": "Mapea la cadena de datos del programa.",
            "cta_body": "Trae un flujo, una plantilla de informe o un problema de datos recurrente. Trazaremos dónde nace la información, dónde se rompe y qué debe cambiar primero.",
            "cta_label": "Empezar por el flujo",
        },
        "funding": {
            "title": "CRM de captación, donantes, donaciones y subvenciones | EdZola",
            "description": "Conecta la captación, la relación con donantes, las donaciones, subvenciones, presupuestos, utilización e informes.",
            "eyebrow": "Sistemas de financiación y relaciones",
            "h1": "Sigue cada relación y cada rupia desde la primera conversación hasta el informe final.",
            "lead": "Diseñamos un ciclo compartido para prospectos, donantes, donaciones, propuestas, subvenciones, obligaciones, tramos, presupuestos, utilización y renovaciones.",
            "section_title": "Captar fondos, gestionar subvenciones e informar no deberían vivir en sistemas separados.",
            "section_body": "Cuando las relaciones, las promesas y el uso del dinero se separan, la organización pierde continuidad y reconstruye el contexto a mano.",
            "cards": [("Pipeline invisible", "Las oportunidades y los seguimientos dependen de recuerdos y hojas personales."), ("Historia fragmentada", "Comunicaciones, donaciones y documentos no forman una relación completa."), ("Obligaciones dispersas", "Presupuestos, tramos, entregables e informes se controlan en lugares distintos.")],
            "workflow": ["Identificar y cualificar", "Conversación y propuesta", "Compromiso y acuerdo", "Donación o tramo", "Ejecución y utilización", "Informe, cuidado y renovación"],
            "modules_title": "Un ciclo de financiación conectado, con las vistas que cada equipo necesita.",
            "modules": [("CRM de captación", "Prospectos, oportunidades, próximos pasos, propuestas y previsiones."), ("Donantes y donaciones", "Perfiles, preferencias, campañas, pagos, recibos y cuidado."), ("Subvenciones y fondos", "Acuerdos, presupuestos, tramos, entregables, restricciones y renovaciones."), ("Informes y cumplimiento", "Utilización, documentos, fechas, aprobaciones y evidencia trazable.")],
            "transform_title": "La financiación se vuelve más fiable cuando las promesas pueden encontrarse con la ejecución.",
            "transform_body": "Conectamos relaciones y obligaciones con programas, evidencia, gastos y responsables en una secuencia que preserva la continuidad del equipo.",
            "cta_title": "Revisa el ciclo completo de financiación.",
            "cta_body": "Trae un pipeline, informe de donante, presupuesto de subvención o proceso de recibos. Identificaremos el primer traspaso que merece arreglo.",
            "cta_label": "Empezar por la relación",
        },
        "people": {
            "title": "Sistemas de RR. HH. y operaciones de personas | EdZola",
            "description": "Conecta selección, expedientes, incorporación, permisos, asistencia, nómina, desempeño, gastos y salida.",
            "eyebrow": "Sistemas de personas y RR. HH.",
            "h1": "Da a cada persona empleada un recorrido fiable desde la contratación hasta la salida.",
            "lead": "Diseñamos sistemas de RR. HH. para equipos distribuidos, con políticas claras, datos fiables, autoservicio útil y traspasos que no dependen de una sola persona.",
            "section_title": "Las personas sienten cada vacío del proceso.",
            "section_body": "Cuando los datos, políticas y aprobaciones se separan, RR. HH. persigue información y el personal recibe respuestas diferentes.",
            "cards": [("Datos dispersos", "Expedientes, contratos, documentos y cambios viven en carpetas y hojas."), ("Trabajo repetido", "Asistencia, permisos, nómina y gastos requieren conciliación mensual."), ("Experiencia desigual", "La incorporación, el desempeño y la salida cambian según el equipo.")],
            "workflow": ["Planificar y contratar", "Seleccionar y verificar", "Incorporar y equipar", "Asistencia, permisos y nómina", "Desarrollo y desempeño", "Salida y continuidad"],
            "modules_title": "Un registro fiable para las personas y los procesos que dependen de él.",
            "modules": [("RR. HH. central", "Perfiles, puestos, equipos, ubicaciones, documentos y cambios."), ("Tiempo y nómina", "Asistencia, permisos, turnos, variables y controles previos a nómina."), ("Talento y desempeño", "Vacantes, candidaturas, incorporación, objetivos, revisiones y aprendizaje."), ("Servicios al personal", "Solicitudes, cartas, gastos, activos, consultas y salida.")],
            "transform_title": "Un sistema de personas puede estabilizar la organización mientras avanza un cambio mayor.",
            "transform_body": "Roles, equipos, líneas de reporte y accesos limpios facilitan conectar después proyectos, finanzas, subvenciones y programas.",
            "cta_title": "Revisa el ciclo de vida de las personas.",
            "cta_body": "Trae formularios, la lista mensual de nómina, la política de permisos o el flujo de incorporación. Identificaremos la primera entrega útil.",
            "cta_label": "Empezar por el flujo de personas",
        },
        "finance": {
            "title": "Sistemas de finanzas, gastos, proyectos y operaciones | EdZola",
            "description": "Conecta presupuestos, gastos, utilización de fondos, proyectos, tareas, aprobaciones y traspasos contables.",
            "eyebrow": "Sistemas de finanzas y operaciones",
            "h1": "Haz que presupuestos, aprobaciones, proyectos y ejecución avancen juntos.",
            "lead": "Diseñamos la capa operativa alrededor de la contabilidad: control presupuestario, gastos, utilización, proyectos, responsables, documentos, aprobaciones y comunicación.",
            "section_title": "El plan, el trabajo y el gasto se separan.",
            "section_body": "La contabilidad puede ser correcta mientras responsables de proyecto siguen sin ver presión presupuestaria, aprobaciones pendientes o evidencia faltante.",
            "cards": [("Niebla de aprobaciones", "Las solicitudes viajan por chat y correo sin propiedad ni estado claro."), ("Datos tardíos", "La visibilidad presupuestaria llega después de tomar la decisión."), ("Trabajo disperso", "Tareas, riesgos, documentos, tiempo y costes viven en herramientas separadas.")],
            "workflow": ["Plan, presupuesto y responsables", "Solicitud y aprobación", "Proyecto, tarea y compromiso", "Gasto, factura y pago", "Real, asignación y variación", "Evidencia, revisión y nueva previsión"],
            "modules_title": "Da a cada equipo la vista correcta sin reconstruir la contabilidad.",
            "modules": [("Presupuestos y revisiones", "Estructuras por programa, proyecto, subvención y centro de coste."), ("Solicitudes y aprobaciones", "Compras, viajes, anticipos, gastos y pagos con umbrales y evidencia."), ("Proyectos y trabajo", "Hitos, tareas, responsables, dependencias, riesgos, documentos y decisiones."), ("Traspaso contable", "Registros validados, conciliación e integraciones con Zoho Books o Tally.")],
            "transform_title": "Operaciones es donde los sistemas separados se conectan o crean más trabajo.",
            "transform_body": "Secuenciamos este pilar cuando los registros de programas, financiación o personas ya son fiables, para evitar multiplicar la conciliación.",
            "cta_title": "Audita los traspasos operativos.",
            "cta_body": "Trae un presupuesto, aprobación, proyecto o proceso de gastos. Identificaremos dónde se separan propiedad, datos y decisiones.",
            "cta_label": "Empezar por el traspaso roto",
        },
        "procurement": {
            "title": "Sistemas de compras, órdenes e inventario | EdZola",
            "description": "Conecta solicitudes de compra, presupuestos, proveedores, cotizaciones, órdenes, recepciones, facturas, pagos e inventario.",
            "eyebrow": "Compras e inventario",
            "h1": "Sigue cada compra desde la necesidad hasta la recepción, el pago y el inventario.",
            "lead": "Diseñamos sistemas de compras para ONG y empresas que conectan solicitudes, presupuestos, proveedores, cotizaciones, aprobaciones, órdenes de compra, recepción de bienes o servicios, facturas, pagos e inventario.",
            "section_title": "Una compra pierde control cuando cada equipo ve solo una parte.",
            "section_body": "El correo, las hojas y los sistemas contables pueden registrar fragmentos del proceso sin mostrar el compromiso completo, la excepción actual ni quién debe actuar.",
            "cards": [("Aprobaciones opacas", "La solicitud se mueve entre correos y chats sin una cola, un responsable o un historial fiable."), ("Compromisos tardíos", "El presupuesto se revisa después de decidir, y las órdenes se crean cuando el gasto ya ocurrió."), ("Recepción desconectada", "Bienes, servicios, facturas, existencias y pagos no comparten una referencia trazable.")],
            "workflow": ["Necesidad y solicitud", "Presupuesto y política", "Proveedor y cotizaciones", "Aprobación y orden", "Recepción o conformidad", "Factura, pago y conciliación"],
            "modules_title": "Un flujo configurable de solicitud a conciliación.",
            "modules": [("Solicitudes y presupuesto", "Propósito, entidad, proyecto, subvención o centro de coste, partidas, fechas y comprobaciones presupuestarias."), ("Proveedores y cotizaciones", "Alta controlada, documentos, categorías, precios, plazos, comparaciones y justificación de selección."), ("Aprobaciones y órdenes", "Matrices por rol y valor, separación de funciones, numeración, versiones, anticipos y saldos."), ("Recepción, inventario y pago", "GRN o conformidad de servicio, entregas parciales, variaciones, activos o existencias, factura y traspaso contable.")],
            "transform_title": "Las compras conectan financiación, programas, personas, activos y contabilidad.",
            "transform_body": "Puede empezar como un flujo concreto y convertirse en una etapa de transformación más amplia cuando presupuestos, maestros, inventario y sistemas financieros se conectan en secuencia.",
            "cta_title": "Traza una compra real de principio a fin.",
            "cta_body": "Trae una solicitud, una cadena de aprobación, una orden o un problema de inventario. Identificaremos dónde se pierde el contexto y cuál es el primer cambio útil.",
            "cta_label": "Revisar el flujo de compras",
        },
    },
    "pt": {},
}

# Portuguese content mirrors the same information architecture with native copy.
PAGES["pt"] = {
    "hub": {
        "title": "Sistemas para ONGs: programas, captação, RH e operações | EdZola",
        "description": "Sistemas conectados para programas, evidências, captação, doadores, grants, RH, finanças e operações, com transformação digital em etapas.",
        "eyebrow": "Sistemas por necessidade organizacional",
        "h1": "Sua missão é específica. Os sistemas por trás dela se repetem.",
        "lead": "A EdZola projeta os sistemas conectados que ajudam organizações de impacto a executar programas, comprovar resultados, gerir recursos, apoiar pessoas e coordenar o trabalho. Comece por um fluxo quebrado ou transforme a organização em uma sequência deliberada.",
        "intro": "Quatro pilares conectados",
        "intro_body": "Cada pilar pode funcionar sozinho, conectar-se ao que você já usa ou virar uma etapa de um roteiro para toda a organização.",
        "pillars": [("programme", "01 · Programas e evidências", "Saiba quem recebeu o quê, o que mudou e o que precisa de atenção.", "MIS de programas, casos, indicadores, acompanhamentos, painéis e relatórios em torno de um registro útil."), ("funding", "02 · Captação e relacionamentos", "Acompanhe recursos e relacionamentos da primeira conversa ao relatório final.", "CRM de captação, doadores, doações, grants, orçamentos, parcelas, utilização e renovações."), ("people", "03 · Pessoas e RH", "Dê a cada pessoa uma jornada confiável da contratação ao desligamento.", "Recrutamento, cadastro, onboarding, licenças, presença, folha, desempenho e despesas."), ("finance", "04 · Finanças e operações", "Faça orçamentos, aprovações, projetos e entrega avançarem juntos.", "Controle orçamentário, despesas, projetos, tarefas, documentos, campanhas e repasses contábeis.")],
        "transform_title": "Transforme a organização inteira sem uma implantação de uma vez.",
        "transform_body": "Reduzimos a tensão ao rastrear como trabalho, dados e decisões passam pelos processos e sistemas existentes. Depois sequenciamos a mudança para que cada entrega alivie pressão antes da próxima.",
        "steps": ["Mapear o trabalho real", "Simplificar primeiro", "Estabilizar os registros centrais", "Conectar as passagens", "Automatizar e aprender"],
        "cta_title": "Onde o trabalho está quebrando hoje?", "cta_body": "Traga o fluxo, a planilha, o relatório ou a passagem que cria mais pressão. Ajudaremos a decidir se vale reparar um sistema ou planejar uma transformação mais ampla.", "cta_label": "Mapear o próximo passo útil",
    },
    "programme": {
        "title": "MIS de programas, gestão de casos e sistemas de MEL | EdZola", "description": "Sistemas de programas, casos, monitoramento, avaliação e relatórios que conectam a entrega no campo a decisões confiáveis.", "eyebrow": "Sistemas de programas e evidências", "h1": "Saiba quem recebeu o quê, o que mudou e o que precisa de atenção.", "lead": "Projetamos MIS de programas, gestão de casos, monitoramento, avaliação e relatórios em torno da jornada real de participantes, parceiros e equipes de campo.", "section_title": "O relatório só é confiável quando a jornada por trás dele também é.", "section_body": "Os problemas costumam começar antes: identidades duplicadas, etapas confusas, atrasos sem conexão, indicadores mudando ou acompanhamentos fora do sistema.", "cards": [("Jornadas fragmentadas", "A mesma pessoa aparece em várias planilhas e ninguém vê a história completa."), ("Visibilidade tardia", "Gestores descobrem abandonos depois que o programa terminou."), ("Pressão de relatórios", "Cada financiador recebe uma versão reconstruída manualmente.")], "workflow": ["Desenho, resultados e metas", "Inscrição, consentimento e identidade", "Serviços, presença e casos", "Avaliações, encaminhamentos e marcos", "Acompanhamento, resultados e qualidade", "Decisões, aprendizado e relatórios"], "modules_title": "Um sistema de trabalho para a linha de frente, não apenas uma base de relatórios.", "modules": [("Participantes e famílias", "Identidade, consentimento, relações, elegibilidade, localização e histórico."), ("Programas e serviços", "Turmas, sessões, presença, direitos, parceiros e atividades de campo."), ("Casos e encaminhamentos", "Necessidades, riscos, planos, notas, documentos e acompanhamentos."), ("Experiência de campo", "Formulários móveis, offline, portais, validações e revisão.")], "transform_title": "Dados de programa ficam mais úteis quando encontram captação, pessoas e finanças.", "transform_body": "Estabilizamos primeiro a jornada do participante e depois conectamos relatórios, obrigações, alocação de equipe, despesas e decisões.", "cta_title": "Mapeie a cadeia de dados do programa.", "cta_body": "Traga um fluxo, modelo de relatório ou problema recorrente. Vamos rastrear onde a informação nasce, onde quebra e o que precisa mudar primeiro.", "cta_label": "Começar pelo fluxo",
    },
    "funding": {
        "title": "CRM de captação, doadores, doações e grants | EdZola", "description": "Conecte captação, relacionamento com doadores, doações, grants, orçamentos, utilização e relatórios.", "eyebrow": "Sistemas de captação e relacionamentos", "h1": "Acompanhe cada relacionamento e cada recurso da primeira conversa ao relatório final.", "lead": "Projetamos um ciclo compartilhado para prospects, doadores, doações, propostas, grants, obrigações, parcelas, orçamentos, utilização e renovações.", "section_title": "Captar, gerir grants e prestar contas não deveriam viver em sistemas separados.", "section_body": "Quando relacionamentos, promessas e uso do recurso se separam, a organização perde continuidade e reconstrói o contexto manualmente.", "cards": [("Pipeline invisível", "Oportunidades e acompanhamentos dependem de memória e planilhas pessoais."), ("Histórico fragmentado", "Comunicações, doações e documentos não formam uma relação completa."), ("Obrigações dispersas", "Orçamentos, parcelas, entregas e relatórios ficam em lugares diferentes.")], "workflow": ["Identificar e qualificar", "Conversa e proposta", "Compromisso e acordo", "Doação ou parcela", "Entrega e utilização", "Relatório, cuidado e renovação"], "modules_title": "Um ciclo de captação conectado, com a visão certa para cada equipe.", "modules": [("CRM de captação", "Prospects, oportunidades, próximos passos, propostas e previsões."), ("Doadores e doações", "Perfis, preferências, campanhas, pagamentos, recibos e relacionamento."), ("Grants e fundos", "Acordos, orçamentos, parcelas, entregas, restrições e renovações."), ("Relatórios e conformidade", "Utilização, documentos, prazos, aprovações e evidências rastreáveis.")], "transform_title": "A captação fica mais confiável quando promessas encontram a entrega.", "transform_body": "Conectamos relacionamentos e obrigações a programas, evidências, despesas e responsáveis em uma sequência que preserva a continuidade.", "cta_title": "Revise o ciclo completo de captação.", "cta_body": "Traga um pipeline, relatório de doador, orçamento de grant ou processo de recibos. Identificaremos a primeira passagem que vale corrigir.", "cta_label": "Começar pelo relacionamento",
    },
    "people": {
        "title": "Sistemas de RH e operações de pessoas | EdZola", "description": "Conecte recrutamento, cadastros, onboarding, licenças, presença, folha, desempenho, despesas e desligamento.", "eyebrow": "Sistemas de pessoas e RH", "h1": "Dê a cada pessoa uma jornada confiável da contratação ao desligamento.", "lead": "Projetamos sistemas de RH para equipes distribuídas, com políticas claras, dados confiáveis, autosserviço útil e passagens que não dependem de uma só pessoa.", "section_title": "As pessoas sentem cada lacuna do processo.", "section_body": "Quando dados, políticas e aprovações se separam, o RH persegue informações e a equipe recebe respostas diferentes.", "cards": [("Dados dispersos", "Cadastros, contratos, documentos e mudanças vivem em pastas e planilhas."), ("Trabalho repetido", "Presença, licenças, folha e despesas exigem conciliação mensal."), ("Experiência desigual", "Onboarding, desempenho e desligamento mudam conforme a equipe.")], "workflow": ["Planejar e contratar", "Selecionar e verificar", "Integrar e equipar", "Presença, licenças e folha", "Desenvolvimento e desempenho", "Desligamento e continuidade"], "modules_title": "Um registro confiável para as pessoas e os processos que dependem dele.", "modules": [("RH central", "Perfis, cargos, equipes, locais, documentos e mudanças."), ("Tempo e folha", "Presença, licenças, escalas, variáveis e controles antes da folha."), ("Talentos e desempenho", "Vagas, candidaturas, onboarding, metas, avaliações e aprendizagem."), ("Serviços à equipe", "Solicitações, cartas, despesas, ativos, dúvidas e desligamento.")], "transform_title": "Um sistema de pessoas pode estabilizar a organização enquanto uma mudança maior avança.", "transform_body": "Papéis, equipes, linhas de reporte e acessos limpos facilitam conectar projetos, finanças, grants e programas depois.", "cta_title": "Revise o ciclo de vida das pessoas.", "cta_body": "Traga formulários, a lista mensal da folha, a política de licenças ou o fluxo de onboarding. Identificaremos a primeira entrega útil.", "cta_label": "Começar pelo fluxo de pessoas",
    },
    "finance": {
        "title": "Sistemas de finanças, despesas, projetos e operações | EdZola", "description": "Conecte orçamentos, despesas, utilização de fundos, projetos, tarefas, aprovações e repasses contábeis.", "eyebrow": "Sistemas de finanças e operações", "h1": "Faça orçamentos, aprovações, projetos e entrega avançarem juntos.", "lead": "Projetamos a camada operacional ao redor da contabilidade: controle orçamentário, despesas, utilização, projetos, responsáveis, documentos, aprovações e comunicação.", "section_title": "O plano, o trabalho e o gasto se afastam.", "section_body": "A contabilidade pode estar correta enquanto donos de projeto ainda não enxergam pressão orçamentária, aprovações pendentes ou evidências faltando.", "cards": [("Névoa de aprovações", "Solicitações passam por chat e e-mail sem dono nem status claros."), ("Dados tardios", "A visibilidade do orçamento chega depois que a decisão foi tomada."), ("Trabalho disperso", "Tarefas, riscos, documentos, tempo e custos vivem em ferramentas separadas.")], "workflow": ["Plano, orçamento e responsáveis", "Solicitação e aprovação", "Projeto, tarefa e compromisso", "Despesa, fatura e pagamento", "Realizado, alocação e variação", "Evidência, revisão e nova previsão"], "modules_title": "Dê a cada equipe a visão certa sem reconstruir a contabilidade.", "modules": [("Orçamentos e revisões", "Estruturas por programa, projeto, grant e centro de custo."), ("Solicitações e aprovações", "Compras, viagens, adiantamentos, despesas e pagamentos com limites e evidências."), ("Projetos e trabalho", "Marcos, tarefas, responsáveis, dependências, riscos, documentos e decisões."), ("Repasse contábil", "Registros validados, conciliação e integrações com Zoho Books ou Tally.")], "transform_title": "Operações é onde sistemas separados se conectam ou criam mais trabalho.", "transform_body": "Sequenciamos este pilar quando registros de programas, captação ou pessoas já são confiáveis, para não multiplicar a conciliação.", "cta_title": "Audite as passagens operacionais.", "cta_body": "Traga um orçamento, aprovação, projeto ou processo de despesas. Identificaremos onde responsabilidade, dados e decisões se separam.", "cta_label": "Começar pela passagem quebrada",
    },
    "procurement": {
        "title": "Sistemas de compras, pedidos e estoque | EdZola", "description": "Conecte solicitações, orçamento, fornecedores, cotações, pedidos, recebimento, faturas, pagamentos e estoque.", "eyebrow": "Compras e estoque", "h1": "Acompanhe cada compra da necessidade ao recebimento, pagamento e estoque.", "lead": "Projetamos sistemas de compras para ONGs e empresas que conectam solicitações, orçamento, fornecedores, cotações, aprovações, pedidos de compra, recebimento de bens ou serviços, faturas, pagamentos e estoque.", "section_title": "Uma compra perde controle quando cada equipe enxerga apenas uma parte.", "section_body": "E-mail, planilhas e sistemas contábeis podem registrar pedaços do processo sem mostrar o compromisso completo, a exceção atual ou quem precisa agir.", "cards": [("Aprovações opacas", "A solicitação passa por e-mail e chat sem fila, responsável ou histórico confiável."), ("Compromissos tardios", "O orçamento é verificado depois da decisão e os pedidos aparecem quando a despesa já ocorreu."), ("Recebimento desconectado", "Bens, serviços, faturas, estoque e pagamentos não compartilham uma referência rastreável.")], "workflow": ["Necessidade e solicitação", "Orçamento e política", "Fornecedor e cotações", "Aprovação e pedido", "Recebimento ou aceite", "Fatura, pagamento e conciliação"], "modules_title": "Um fluxo configurável da solicitação à conciliação.", "modules": [("Solicitações e orçamento", "Finalidade, entidade, projeto, grant ou centro de custo, itens, datas e verificações de orçamento."), ("Fornecedores e cotações", "Cadastro controlado, documentos, categorias, preços, prazos, comparações e justificativa de escolha."), ("Aprovações e pedidos", "Matrizes por papel e valor, segregação de funções, numeração, versões, adiantamentos e saldos."), ("Recebimento, estoque e pagamento", "GRN ou aceite de serviço, entregas parciais, divergências, ativos ou estoque, fatura e repasse contábil.")], "transform_title": "Compras conectam captação, programas, pessoas, ativos e contabilidade.", "transform_body": "Pode começar como um fluxo específico e virar uma etapa de transformação maior quando orçamentos, cadastros, estoque e sistemas financeiros são conectados em sequência.", "cta_title": "Mapeie uma compra real de ponta a ponta.", "cta_body": "Traga uma solicitação, cadeia de aprovação, pedido ou problema de estoque. Vamos identificar onde o contexto se perde e qual é a primeira mudança útil.", "cta_label": "Revisar o fluxo de compras",
    },
}

PROOFS = {
    "hub": [("Compass MIS", "https://www.edzola.com/post/compass-mis-transforming-state-wide-teacher-training-with-tech"), ("CRM de NeevJivan", "https://www.edzola.com/post/neevjivan-foundation-streamlining-and-tracking-fundraising-and-donor-engagement-with-zoho-crm"), ("RH da Aangan Trust", "https://www.edzola.com/post/edg-aangan-trust-streamlining-hr-operations-and-employee-data-management-through-zoho-people")],
    "programme": [("Compass MIS", "https://www.edzola.com/post/compass-mis-transforming-state-wide-teacher-training-with-tech"), ("TRRAIN", "https://www.edzola.com/post/edg-trust-for-retailers-retail-associates-of-india-streamlining-program-management"), ("TAP India Foundation", "https://www.edzola.com/post/tap-india-foundation-tracking-out-of-school-children-data-with-zoho-creator")],
    "funding": [("NeevJivan Foundation", "https://www.edzola.com/post/neevjivan-foundation-streamlining-and-tracking-fundraising-and-donor-engagement-with-zoho-crm"), ("CRM para ONG", "https://www.edzola.com/post/how-a-crm-saved-me-from-losing-my-mind-and-why-every-ngo-needs-one"), ("Gestão de grants", "https://www.edzola.com/post/technology-enabled-grant-management-innovations-and-best-practices")],
    "people": [("Aangan Trust", "https://www.edzola.com/post/edg-aangan-trust-streamlining-hr-operations-and-employee-data-management-through-zoho-people"), ("HRMS para ONG", "https://www.edzola.com/post/the-ultimate-guide-to-hrms-for-non-profits-streamlining-hr-processes-with-zoho-people"), ("Implementação de HRMS", "https://www.edzola.com/post/overcoming-implementation-challenges-in-hr-management-systems")],
    "finance": [("Aria CFO Services", "https://www.edzola.com/post/edg-aria-cfo-services-effective-project-management-and-team-collaboration-with-zoho-projects"), ("Zoho Books para ONG", "https://www.edzola.com/post/top-5-reasons-why-zoho-books-is-your-ideal-solution-for-non-profit-accounting-management"), ("Operações com Zoho Creator", "https://www.edzola.com/post/streamlining-non-profit-operations-with-zoho-creator-apps")],
    "procurement": [("Zoho Books para ONG", "https://www.edzola.com/post/top-5-reasons-why-zoho-books-is-your-ideal-solution-for-non-profit-accounting-management"), ("Operações com Zoho Creator", "https://www.edzola.com/post/streamlining-non-profit-operations-with-zoho-creator-apps"), ("Aria CFO Services", "https://www.edzola.com/post/edg-aria-cfo-services-effective-project-management-and-team-collaboration-with-zoho-projects")],
}

RESOURCES = {
    "hub": [("Como as organizações sem fins lucrativos realmente funcionam", "/thinking/how-nonprofits-operate/"), ("Construindo tecnologia que se sustenta", "/field-guides/technology-that-sticks/"), ("Cinco etapas para a transformação digital", "https://www.edzola.com/post/5-steps-to-digital-transformation-for-non-profits-a-comprehensive-guide")],
    "programme": [("O que é um MIS para ONGs?", "https://www.edzola.com/post/what-is-a-management-information-system-mis-for-nonprofits-the-complete-2026-guide"), ("A jornada do participante", "/thinking/how-nonprofits-operate/#people"), ("Dados, M&E e fluxos", "/thinking/how-nonprofits-operate/#evidence")],
    "funding": [("O fluxo do dinheiro", "/thinking/how-nonprofits-operate/#money"), ("Avalie sua tecnologia", "https://www.edzola.com/post/how-to-perform-tech-evaluation-criteria-for-technology-assessment-in-nonprofits"), ("Comece pela necessidade humana", "https://www.edzola.com/post/stop-chasing-tools-start-with-the-human-need")],
    "people": [("Avalie o que você já tem", "https://www.edzola.com/post/how-to-perform-tech-evaluation-criteria-for-technology-assessment-in-nonprofits"), ("Rica em missão, pobre em sistemas", "/field-guides/technology-that-sticks/mission-rich-systems-poor/"), ("Como novos padrões ganham adesão", "/field-guides/technology-that-sticks/warmth-is-how-standards-travel/")],
    "finance": [("Orçamento, alocação e utilização", "/thinking/how-nonprofits-operate/#money"), ("Tecnologia, automação e IA", "/thinking/how-nonprofits-operate/#systems"), ("Superando silos de dados", "https://www.edzola.com/post/unlocking-nonprofit-efficiency-overcoming-data-silos-and-centralizing-your-systems")],
    "procurement": [("O fluxo do dinheiro", "/thinking/how-nonprofits-operate/#money"), ("Avalie sua tecnologia", "https://www.edzola.com/post/how-to-perform-tech-evaluation-criteria-for-technology-assessment-in-nonprofits"), ("Superando silos de dados", "https://www.edzola.com/post/unlocking-nonprofit-efficiency-overcoming-data-silos-and-centralizing-your-systems")],
}

SPANISH_TITLES = {
    "RH da Aangan Trust": "RR. HH. de Aangan Trust",
    "Gestão de grants": "Gestión de subvenciones",
    "Implementação de HRMS": "Implementación de HRMS",
    "Operações com Zoho Creator": "Operaciones con Zoho Creator",
    "Como as organizações sem fins lucrativos realmente funcionam": "Cómo funcionan realmente las organizaciones sin fines de lucro",
    "Construindo tecnologia que se sustenta": "Construir tecnología que se mantenga",
    "Cinco etapas para a transformação digital": "Cinco etapas para la transformación digital",
    "O que é um MIS para ONGs?": "¿Qué es un MIS para ONG?",
    "A jornada do participante": "El recorrido del participante",
    "Dados, M&E e fluxos": "Datos, M&E y flujos",
    "O fluxo do dinheiro": "El flujo del dinero",
    "Avalie sua tecnologia": "Evalúa tu tecnología",
    "Comece pela necessidade humana": "Empieza por la necesidad humana",
    "Avalie o que você já tem": "Evalúa lo que ya tienes",
    "Rica em missão, pobre em sistemas": "Rica en misión, pobre en sistemas",
    "Como novos padrões ganham adesão": "Cómo se adoptan los nuevos estándares",
    "Orçamento, alocação e utilização": "Presupuesto, asignación y utilización",
    "Tecnologia, automação e IA": "Tecnología, automatización e IA",
    "Superando silos de dados": "Superar los silos de datos",
}


def route(locale, key):
    slug = SLUGS[key]
    return f"/{locale}/verticals/" + (f"{slug}/" if slug else "")


def language_links(locale, key, css_class):
    links = []
    for code, label in (("en", "EN"), ("es", "ES"), ("pt", "PT")):
        href = f"/verticals/{SLUGS[key] + '/' if SLUGS[key] else ''}" if code == "en" else route(code, key)
        current = ' aria-current="true"' if code == locale else ""
        links.append(f'<a href="{href}" hreflang="{code}" lang="{code}"{current}>{label}</a>')
    return f'<nav class="{css_class}" aria-label="Idioma">' + "".join(links) + "</nav>"


def navigation(locale, key):
    c = COMMON[locale]
    vr = c["vertical_root"]
    programme_short = "MIS, casos y MEL" if locale == "es" else "MIS, casos e MEL"
    funding_short = "CRM, donantes y subvenciones" if locale == "es" else "CRM, doadores e grants"
    vertical_links = (
        f'<a href="{vr}">{escape(c["all"])}</a>'
        f'<a href="{vr}programme-evidence-systems/">{escape(c["programme"])}</a>'
        f'<a href="{vr}fundraising-donor-grant-systems/">{escape(c["funding"])}</a>'
        f'<a href="{vr}people-hr-systems/">{escape(c["people"])}</a>'
        f'<a href="{vr}finance-operations-systems/">{escape(c["finance"])}</a>'
        f'<a href="{vr}procurement-inventory-systems/">{escape(c["procurement"])}</a>'
    )
    return f'''<header class="site-header"><div class="wrap nav-shell"><a class="brand" href="{c['home']}">edzola.ai</a>
<nav class="primary-nav" aria-label="Principal"><a href="{c['home']}#model">{escape(c['what'])}</a><details class="nav-group"><summary aria-current="page">{escape(c['verticals'])}</summary><div class="mega"><div class="mega-col"><h3>{escape(c['programme'])}</h3><a href="{vr}programme-evidence-systems/">{escape(programme_short)}</a></div><div class="mega-col"><h3>{escape(c['funding'])}</h3><a href="{vr}fundraising-donor-grant-systems/">{escape(funding_short)}</a></div><div class="mega-col"><h3>{escape(c['people'])} &amp; {escape(c['finance'])}</h3><a href="{vr}people-hr-systems/">{escape(c['people'])}</a><a href="{vr}finance-operations-systems/">{escape(c['finance'])}</a><a href="{vr}procurement-inventory-systems/">{escape(c['procurement'])}</a></div><a class="mega-all" href="{vr}"><span>{escape(c['all'])}</span><span>→</span></a></div></details><a href="/sectors/">{escape(c['sectors'])}</a><a href="{c['home']}impact-os/">ImpactOS</a><a href="/thinking/">{escape(c['thinking'])}</a><a href="{c['home']}about/">{escape(c['about'])}</a></nav>
{language_links(locale, key, 'nav-lang')}<a class="pill primary header-cta" href="#contact-form">{escape(c['talk'])}</a>
<details class="mobile-menu"><summary>{escape(c['menu'])}</summary><div class="mobile-panel">{language_links(locale, key, 'mobile-lang')}<a href="{c['home']}#model">{escape(c['what'])}</a><details><summary>{escape(c['verticals'])}</summary>{vertical_links}</details><a href="/sectors/">{escape(c['sectors'])}</a><a href="{c['home']}impact-os/">ImpactOS</a><a href="/thinking/">{escape(c['thinking'])}</a><a href="{c['home']}about/">{escape(c['about'])}</a><a href="#contact-form">{escape(c['talk'])}</a></div></details></div></header>'''


def schema(locale, key, page, canonical):
    language = "es-419" if locale == "es" else "pt-BR"
    graph = [
        {
            "@type": "Organization",
            "@id": "https://edzola.ai/#org",
            "name": "EdZola",
            "legalName": "EdZola Technologies Private Limited",
            "url": "https://edzola.ai/",
            "email": "reachus@edzola.com",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Coimbatore",
                "addressRegion": "Tamil Nadu",
                "addressCountry": "IN",
            },
        },
        {
            "@type": "CollectionPage" if key == "hub" else "WebPage",
            "@id": canonical + "#page",
            "url": canonical,
            "name": page["title"],
            "description": page["description"],
            "inLanguage": language,
            "dateModified": "2026-10-23",
            "publisher": {"@id": "https://edzola.ai/#org"},
        },
    ]
    if key == "hub":
        graph[1]["hasPart"] = [
            {"@type": "WebPage", "url": f"https://edzola.ai{route(locale, child)}"}
            for child in ("programme", "funding", "people", "finance", "procurement")
        ]
    else:
        service_id = canonical + "#service"
        graph[1]["about"] = {"@id": service_id}
        graph.append({
            "@type": "Service",
            "@id": service_id,
            "name": page["h1"],
            "serviceType": page["eyebrow"],
            "description": page["lead"],
            "url": canonical,
            "provider": {"@id": "https://edzola.ai/#org"},
            "areaServed": "Worldwide",
            "audience": {"@type": "Audience", "audienceType": "Nonprofits and social-impact organisations"},
        })
        graph.append({
            "@type": "BreadcrumbList",
            "@id": canonical + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": COMMON[locale]["verticals"], "item": f"https://edzola.ai{route(locale, 'hub')}"},
                {"@type": "ListItem", "position": 2, "name": page["eyebrow"], "item": canonical},
            ],
        })
        graph[1]["breadcrumb"] = {"@id": canonical + "#breadcrumb"}
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def head(locale, key, page):
    canonical = f"https://edzola.ai{route(locale, key)}"
    en_path = f"/verticals/{SLUGS[key] + '/' if SLUGS[key] else ''}"
    return f'''<!doctype html><html lang="{COMMON[locale]['html_lang']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(page['title'])}</title><meta name="description" content="{escape(page['description'], quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="https://edzola.ai{en_path}"><link rel="alternate" hreflang="es" href="https://edzola.ai{route('es', key)}"><link rel="alternate" hreflang="pt-BR" href="https://edzola.ai{route('pt', key)}"><link rel="alternate" hreflang="x-default" href="https://edzola.ai{en_path}">
<meta property="og:type" content="website"><meta property="og:locale" content="{'es_419' if locale == 'es' else 'pt_BR'}"><meta property="og:site_name" content="EdZola"><meta property="og:title" content="{escape(page['h1'], quote=True)}"><meta property="og:description" content="{escape(page['description'], quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://edzola.ai/assets/og-edzola.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(page['h1'], quote=True)}"><meta name="twitter:description" content="{escape(page['description'], quote=True)}"><meta name="twitter:image" content="https://edzola.ai/assets/og-edzola.png">
<script type="application/ld+json">{schema(locale, key, page, canonical)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&amp;family=Figtree:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap"><link rel="stylesheet" href="/assets/verticals.css?v=20261022a"><link rel="stylesheet" href="/assets/crm-webform.css?v=20261019a">
</head><body><a class="skip" href="#main">{escape(COMMON[locale]['skip'])}</a>'''


def proof_and_resources(locale, key):
    c = COMMON[locale]
    title_for = lambda title: SPANISH_TITLES.get(title, title) if locale == "es" else title
    proof = "".join(f'<a class="proof" href="{href}" target="_blank" rel="noopener noreferrer"><small>EdZola</small><h3>{escape(title_for(title))}</h3><p>{escape(c["related"])}.</p><b>{escape(c["case"])}</b></a>' for title, href in PROOFS[key])
    resource_cards = []
    for title, href in RESOURCES[key]:
        external = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
        resource_cards.append(f'<a class="resource" href="{href}"{external}><small>EdZola</small><h3>{escape(title_for(title))}</h3><p>{escape(c["related"])}.</p><b>{escape(c["guide"])}</b></a>')
    resources = "".join(resource_cards)
    return f'<section class="section sunk" id="proof"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{escape(c["related"])}</span><h2>{escape(c["related"])}.</h2></div><p>{escape(c["reference_note"])}</p></div><div class="proof-grid">{proof}</div></div></section><section class="section"><div class="wrap"><div class="resource-grid">{resources}</div></div></section>'


def footer(locale):
    c = COMMON[locale]
    vr = c["vertical_root"]
    return f'''<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="{c['home']}">edzola.ai</a><p>{escape(c['transformation'])}.</p></div><div><h3>{escape(c['verticals'])}</h3><a href="{vr}programme-evidence-systems/">{escape(c['programme'])}</a><a href="{vr}fundraising-donor-grant-systems/">{escape(c['funding'])}</a><a href="{vr}people-hr-systems/">{escape(c['people'])}</a><a href="{vr}finance-operations-systems/">{escape(c['finance'])}</a><a href="{vr}procurement-inventory-systems/">{escape(c['procurement'])}</a></div><div><h3>{escape(c['explore'])}</h3><a href="/sectors/">{escape(c['sectors'])}</a><a href="/thinking/">{escape(c['thinking'])}</a><a href="{c['home']}impact-os/">ImpactOS</a></div><div><h3>{escape(c['start'])}</h3><a href="#contact-form">{escape(c['talk'])}</a><a href="mailto:reachus@edzola.com">reachus@edzola.com</a></div></div><div class="footer-bottom"><span>© EdZola Technologies Private Limited</span><span>{escape(c['country'])}</span></div></div></footer><script src="/assets/verticals-nav.js?v=20261022a"></script><script src="/assets/crm-webform.js?v=20261022a"></script></body></html>'''


def render_hub(locale, page):
    c = COMMON[locale]
    cards = "".join(f'<a class="pillar-card" href="{route(locale, key)}"><span class="number">{escape(label)}</span><h3>{escape(title)}</h3><p>{escape(body)}</p><span class="go">{escape(c[key])} →</span></a>' for key, label, title, body in page["pillars"])
    steps = "".join(f'<article><h3>{escape(step)}</h3><p>{escape(page["transform_body"])}</p></article>' for step in page["steps"])
    return head(locale, "hub", page) + navigation(locale, "hub") + f'''<main id="main"><section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">{escape(page['eyebrow'])}</span><h1>{escape(page['h1'])}</h1><p class="lead">{escape(page['lead'])}</p><div class="hero-actions"><a class="pill primary" href="#pillars">{escape(c['all'])}</a><a class="pill ghost" href="#transformation">{escape(c['transformation'])}</a></div></div><div class="system-map"><div class="map-title"><span>{escape(c['transformation'])}</span><i></i></div><div class="map-core"><b>{escape(page['intro'])}</b><span>{escape(page['intro_body'])}</span></div></div></div></section>
<section class="section" id="pillars"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{escape(page['intro'])}</span><h2>{escape(page['intro'])}</h2></div><p>{escape(page['intro_body'])}</p></div><div class="pillar-grid">{cards}</div><a class="focus-link" href="{route(locale, 'procurement')}"><span>{escape(c['finance'])} · {escape(c['procurement'])}</span><strong>{escape(PAGES[locale]['procurement']['h1'])} →</strong></a></div></section>
<section class="section dark" id="transformation"><div class="wrap"><div class="transform-intro"><span class="eyebrow">{escape(c['transformation'])}</span><h2>{escape(page['transform_title'])}</h2><p>{escape(page['transform_body'])}</p></div><div class="sequence">{steps}</div></div></section>
{proof_and_resources(locale, 'hub')}<section class="section"><div class="wrap"><div class="cta"><div><h2>{escape(page['cta_title'])}</h2><p>{escape(page['cta_body'])}</p></div><a class="pill dark" href="#contact-form">{escape(page['cta_label'])}</a></div></div></section></main>''' + footer(locale)


def render_detail(locale, key, page):
    c = COMMON[locale]
    cards = "".join(f'<article class="problem"><small>0{i}</small><h3>{escape(title)}</h3><p>{escape(body)}</p></article>' for i, (title, body) in enumerate(page["cards"], 1))
    flow = "".join(f'<li>{escape(item)}</li>' for item in page["workflow"])
    modules = "".join(f'<article class="module"><h3>{escape(title)}</h3><p>{escape(body)}</p></article>' for title, body in page["modules"])
    return head(locale, key, page) + navigation(locale, key) + f'''<main id="main"><section class="detail-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{c['vertical_root']}">{escape(c['verticals'])}</a><span>/</span><span aria-current="page">{escape(c[key])}</span></nav><span class="eyebrow">{escape(page['eyebrow'])}</span><h1>{escape(page['h1'])}</h1><p class="lead">{escape(page['lead'])}</p><div class="hero-actions"><a class="pill primary" href="#contact-form">{escape(page['cta_label'])}</a><a class="pill ghost" href="#proof">{escape(c['related'])}</a></div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{escape(page['eyebrow'])}</span><h2>{escape(page['section_title'])}</h2></div><p>{escape(page['section_body'])}</p></div><div class="problem-grid">{cards}</div></div></section>
<section class="section sunk"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Workflow</span><h2>{escape(page['modules_title'])}</h2></div><p>{escape(page['section_body'])}</p></div><ol class="workflow">{flow}</ol></div></section>
<section class="section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{escape(c[key])}</span><h2>{escape(page['modules_title'])}</h2></div><p>{escape(page['lead'])}</p></div><div class="module-grid">{modules}</div></div></section>
<section class="section dark"><div class="wrap"><div class="transform-intro"><span class="eyebrow">{escape(c['transformation'])}</span><h2>{escape(page['transform_title'])}</h2><p>{escape(page['transform_body'])}</p></div><a class="pill primary" href="{c['vertical_root']}#transformation">{escape(c['transformation'])}</a></div></section>
{proof_and_resources(locale, key)}<section class="section"><div class="wrap"><div class="cta"><div><h2>{escape(page['cta_title'])}</h2><p>{escape(page['cta_body'])}</p></div><a class="pill dark" href="#contact-form">{escape(page['cta_label'])}</a></div></div></section></main>''' + footer(locale)


def main():
    for locale, pages in PAGES.items():
        for key, page in pages.items():
            destination = ROOT / route(locale, key).lstrip("/") / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            html = render_hub(locale, page) if key == "hub" else render_detail(locale, key, page)
            destination.write_text(html + "\n", encoding="utf-8")
            print(destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
