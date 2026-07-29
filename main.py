import flet as ft
import uuid
import os
from supabase import create_client, Client

SUPABASE_URL = "https://ysordxpmgdxzfwijduyj.supabase.co"
SUPABASE_KEY = "sb_publishable_cg6I_94Zl0xZ92GB1AO1Xw_Mr6m5Srv"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def main(page: ft.Page):
    COLOR_AZUL_UCM = "#153268"
    COLOR_CELESTE_UCM = "#009FE3"
    COLOR_FONDO = "#F8F9FA"

    page.title = "Proyecto Fondecyt"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.full_screen = True
    page.window.frameless = True
    page.window.width = 450
    page.window.height = 850
    page.bgcolor = COLOR_FONDO
    page.scroll = "auto"
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(
        toolbar_height=80,
        bgcolor=COLOR_FONDO,
        center_title=False,
        title=ft.Image(
                    src="fondecyt.png",
                    height=60,
                    fit=ft.BoxFit.CONTAIN
        )
    )

    page.session.store.set("id_sesion", str(uuid.uuid4()))
    page.session.store.set("nombre_usuario", "")
    page.session.store.set("historial_decisiones", [])
    page.session.store.set("seguro_final", "Ninguno")

    def componente_npc(texto, nombre_imagen="idea.png"):
        return ft.Row(
            controls=[
                # 1. Reducimos el ancho a 70 para eliminar el espacio transparente y acercarlo
                ft.Image(src=nombre_imagen, width=200, height=200, fit="contain"),
                
                ft.Container(
                    content=ft.Text(texto, color=ft.Colors.BLACK_87, size=14),
                    bgcolor=ft.Colors.WHITE,
                    padding=5,
                    # 2. ¡EL TRUCO! Movemos el "0" a top_left. Así el pico nace arriba, a la altura de la boca/cara.
                    border_radius=ft.BorderRadius.only(top_left=20, top_right=20, bottom_right=20, bottom_left=20),
                    border=ft.Border.all(2, COLOR_CELESTE_UCM),
                    width=250,
                    margin=ft.Margin.only(left=-120, bottom=50)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            # 3. Alineamos todo al centro para que el pico coincida perfecto con la cabeza
            vertical_alignment=ft.CrossAxisAlignment.START,
            # 4. Forzamos a Flet a no dejar espacio vacío entre el robot y el globo
            spacing=0 
        )

    def finalizar_simulacion(tipo_seguro):
        page.session.store.set("seguro_final", tipo_seguro)
        mostrar_proyeccion_5_años()

    def cambiar_pantalla(texto_principal, opciones, nombre_rama="General", imagen_npc="idea.png", funcion_atras=None):
        page.controls.clear()

        page.add(
            ft.Container(
                content=componente_npc(texto_principal, imagen_npc),
                margin=ft.Margin.only(bottom=30, top=20)
            )
        )

        def manejar_clic(e, texto_elegido, funcion_destino):
            historial = page.session.store.get("historial_decisiones")
            historial.append((nombre_rama, texto_elegido))
            page.session.store.set("historial_decisiones", historial)

            if funcion_destino:
                funcion_destino()
        
        for texto_boton, funcion_destino in opciones:
            boton = ft.ElevatedButton(
                content=ft.Text(texto_boton, size=14, weight="bold", text_align=ft.TextAlign.CENTER),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=COLOR_CELESTE_UCM
                ),
                width=400,
                height=55,  # Usamos height en lugar de padding para darle buen tamaño
                on_click=lambda e, t=texto_boton, f=funcion_destino: manejar_clic(e, t, f)
            )
            page.add(boton)
            page.add(ft.Divider(height=5, color="transparent"))
        
        # Botón dinámico para regresar en el árbol
        if funcion_atras:
            page.add(ft.Divider(height=10, color="transparent"))
            boton_atras = ft.ElevatedButton(
                content=ft.Text("Volver atrás", size=15, weight="bold"),
                style=ft.ButtonStyle(
                    color=COLOR_AZUL_UCM,
                    bgcolor=ft.Colors.GREY_300
                ),
                width=400,
                height=55,  # Usamos height en lugar de padding
                on_click=lambda e: funcion_atras()
            )
            page.add(boton_atras)
        
        page.update()

    def pantalla_bienvenida():
        page.controls.clear()

        page.add(
            ft.Text(
                "¡Hola! Bienvenido a este simulador de toma de decisiones",
                size=22,
                weight="bold",
                color=COLOR_AZUL_UCM,
                text_align=ft.TextAlign.CENTER
            )
        )
        page.add(ft.Divider(height=10, color="transparent"))

        page.add(
            ft.Text(
                "A través de esta app podrás simular procesos de toma de decisiones en contextos de riesgos e incertidumbre, similares a los que podrías enfrentar en la vida cotidiana. ¡Te invitamos a leer con atención y tomar tu mejor decisión!. Cuéntanos al final qué te pareció el proceso.",
                size=15,
                text_align=ft.TextAlign.JUSTIFY
            )
        )

        page.add(ft.Text("¿Aceptas participar voluntariamente en este estudio?", weight="bold", size=16, text_align=ft.TextAlign.CENTER))
        page.add(ft.Divider(height=10, color="transparent"))

        btn_acepta = ft.ElevatedButton(
            "Sí, acepto participar",
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE, padding=20),
            width=400,
            on_click=lambda e: pantalla_seleccion_simulador(atras=pantalla_bienvenida)
        )

        def rechazo_estudio(e):
            page.controls.clear()
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            
            def volver_al_inicio(e):
                page.vertical_alignment = ft.MainAxisAlignment.START
                pantalla_bienvenida()

            def cerrar_ventana(e):
                page.controls.clear()

                pantalla_despedida = ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "¡Simulación finalizada! Ya puedes devolver o bloquear este dispositivo.",
                                color=ft.Colors.BLACK_87,
                                size=16,
                                text_align=ft.TextAlign.CENTER
                            ),
                            bgcolor=ft.Colors.WHITE,
                            padding=20,
                            border_radius=20,
                            border=ft.Border.all(2, COLOR_CELESTE_UCM),
                            width=350,
                            margin=ft.Margin.only(bottom=20)
                        ),
                        ft.Image(src="adios.png", width=300, height=300, fit="contain")
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0
                )

                page.add(pantalla_despedida)
                page.update()
            
            pantalla_rechazo = ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Has decidico no paticipar. ¡No hay problema, gracias por tu tiempo!",
                            color=ft.Colors.BLACK_87,
                            size=16,
                            text_align=ft.TextAlign.CENTER
                        ),
                        bgcolor=ft.Colors.WHITE,
                        padding=20,
                        border_radius=20,
                        border=ft.Border.all(2, COLOR_CELESTE_UCM),
                        width=350,
                        margin=ft.Margin.only(bottom=20)    
                    ),
                    ft.Image(src="adios.png", width=300, height=300, fit="contain"),

                    ft.Divider(height=20, color="transparent"),
                    ft.ElevatedButton(
                        content=ft.Text("🔄 Volver al inicio"),
                        style=ft.ButtonStyle(bgcolor=COLOR_AZUL_UCM, color=ft.Colors.WHITE),
                        on_click=volver_al_inicio,
                        width=400
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.ElevatedButton(
                        content=ft.Text("❌ Salir del Simulador"),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
                        on_click=cerrar_ventana,
                        width=400
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0
            )
            page.add(pantalla_rechazo)
            page.update()

        btn_rechaza = ft.ElevatedButton(
            "No, rechazo participar",
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE, padding=20),
            width=400, 
            on_click=rechazo_estudio
        )
        
        page.add(btn_acepta, ft.Divider(height=5, color="transparent"), btn_rechaza)
        
        # 4. PIE DE PÁGINA (Texto y Logo adjunto)
        page.add(ft.Divider(height=20, color="transparent"))
        page.add(
            ft.Column(
                controls=[
                    ft.Text(
                        "Recurso desarrollado en el marco del proyecto FONDECYT de Iniciación N°11240150.",
                        size=12,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                        italic=True
                    ),
                    ft.Image(src="fondecyt11240150.png", height=50, fit=ft.BoxFit.CONTAIN)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            )
        )

        page.update()
    
    def pantalla_seleccion_simulador(atras=None):
        page.controls.clear()

        page.add(componente_npc("¡Genial! Por Favor, registra tu nombre y selecciona el simulador al que deseas ingrear.", "idea.png"))

        campo_nombre = ft.TextField(
            label="Tu nombre",
            border_color=COLOR_CELESTE_UCM,
            width=400
        )
        
        def ingresar_grooming(e):
            nombre = campo_nombre.value.strip()
            if len(nombre) < 2:
                campo_nombre.error = "Ingresa un nombre válido"
                page.update()
                return
            
            campo_nombre.error = None

            page.session.store.set("nombre_usuario", nombre)
            pantalla_contexto_grooming(atras=lambda: pantalla_seleccion_simulador(atras))

        def ingresar_medioambiente(e):
            page.snack_bar = ft.SnackBar(ft.Text("Este simulador estará disponible próximamente."))
            page.snack_bar.open = True
            page.update()
        
        tarjeta_grooming = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PETS, size=40, color=COLOR_CELESTE_UCM),
                    ft.Text("Simulador de Negocio de Grooming", weight="bold", size=16),
                    ft.ElevatedButton("Ingresar", style=ft.ButtonStyle(bgcolor=COLOR_CELESTE_UCM, color=ft.Colors.WHITE), on_click=ingresar_grooming)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, width=400
            )
        )

        tarjeta_medioambiente = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ECO, size=40, color=ft.Colors.GREEN_600),
                    ft.Text("Simulador de Decisiones Medioambientales", weight="bold", size=16),
                    ft.ElevatedButton("Próximamente", on_click=ingresar_medioambiente)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, width=400
            )
        )
        
        page.add(campo_nombre, ft.Divider(height=10, color="transparent"), tarjeta_grooming, tarjeta_medioambiente)

        if atras:
            page.add(ft.Divider(height=10, color="transparent"))
            page.add(ft.ElevatedButton("Volver atrás", on_click=lambda e: atras(), width=400, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_300, color=COLOR_AZUL_UCM)))
        page.update()

    def pantalla_contexto_grooming(atras=None):
        page.controls.clear()

        page.vertical_alignment = ft.MainAxisAlignment.START

        texto_contexto = "Contexto: Las tiendas de mascotas y servicios de 'grooming' (peluquería y cuidado animal) han tenido un gran auge durante los últimos años, convirtiéndose en un negocio muy rentable.\n\nEn este simulador, tomarás decisiones para proteger tu inversión inicial."
        elementos = ft.Column(
            controls=[
                componente_npc(texto_contexto, "idea.png"),
                
                # 3. Reducimos el height a 200 para matar el espacio transparente
                ft.Image(src="tienda_mascotas.png", width=400, height=200, fit=ft.BoxFit.CONTAIN, border_radius=10),
                
                ft.ElevatedButton(
                    "Comenzar Simulación",
                    style=ft.ButtonStyle(bgcolor=COLOR_CELESTE_UCM, color=ft.Colors.WHITE, padding=20),
                    width=400,
                    on_click=lambda e: iniciar_seguro(atras=lambda: pantalla_contexto_grooming(atras))
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15 # <--- Esta es la distancia exacta entre el robot, la foto y el botón
        )
        if atras:
            elementos.controls.append(ft.Divider(height=5, color="transparent"))
            elementos.controls.append(ft.ElevatedButton("Volver atrás", on_click=lambda e: atras(), width=400, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_300, color=COLOR_AZUL_UCM, padding=20)))

        page.add(elementos)
        page.update()

        #RAMA DE ACEPTACIÓN DINÁMICA

    def rama_aceptacion_base(funcion_informacion_siguiente, texto_info_siguiente, mostrar_en_seleccion=False, atras=None):
        texto = "¿Qué tipo de seguro deseas evaluar?"

        opciones = [
            ("Seguro Full", lambda: evaluar_seguro("Full", funcion_informacion_siguiente, texto_info_siguiente, lambda: rama_aceptacion_base(funcion_informacion_siguiente, texto_info_siguiente, mostrar_en_seleccion, atras))),
            ("Seguro Parcial", lambda: evaluar_seguro("Parcial", funcion_informacion_siguiente, texto_info_siguiente, lambda: rama_aceptacion_base(funcion_informacion_siguiente, texto_info_siguiente, mostrar_en_seleccion, atras)))
        ]

        # Solo mostramos la 3ra opción aquí si estamos en la primera decisión del inicio (mostrar_en_seleccion=True)
        if mostrar_en_seleccion and funcion_informacion_siguiente and texto_info_siguiente:
            opciones.append((texto_info_siguiente, lambda: funcion_informacion_siguiente(atras=lambda: rama_aceptacion_base(funcion_informacion_siguiente, texto_info_siguiente, mostrar_en_seleccion, atras))))

        cambiar_pantalla(texto, opciones, "Seleccion de Tipo de Seguro", "idea.png", atras)

    def evaluar_seguro(tipo_seguro, funcion_informacion_siguiente, texto_info_siguiente, atras=None):
        if tipo_seguro == "Full":
            texto = "Debes pagar una prima mensual de $90.000.\n\n¿Tomarías el seguro?"
        else:
            texto = "Debes pagar una prima mensual de $40.000.\n\n¿Tomarías el seguro?"
            
        opciones = [
            ("Sí, quiero tomar este seguro", lambda: finalizar_simulacion(tipo_seguro))
        ]

        # En la pantalla de evaluación del precio, SIEMPRE sale la opción de pedir más info (si existe)
        if funcion_informacion_siguiente and texto_info_siguiente:
            opciones.append((texto_info_siguiente, lambda: funcion_informacion_siguiente(atras=lambda: evaluar_seguro(tipo_seguro, funcion_informacion_siguiente, texto_info_siguiente, atras))))

        cambiar_pantalla(texto, opciones, f'Evaluación del Seguro {tipo_seguro}', "idea.png", atras)

    def iniciar_seguro(atras=None):
        page.session.store.set("historial_decisiones", [])
        texto = "Inviertes para iniciar un negocio de grooming para mascotas en un local físico.\n\nUna compañia de seguros te ofrece asegurar tu local. ¿Lo tomarías?"
        texto_info_gastos = "No, necesito más información sobre los gastos y ganancias del negocio antes de tomar una decisión"

        opciones = [
            # AQUÍ ES EL ÚNICO LUGAR DONDE ACTIVAMOS LA LLAVE (True) PARA MOSTRAR LAS 3 OPCIONES
            ("Sí, lo tomaría", lambda: rama_aceptacion_base(rama_gastos, texto_info_gastos, True, lambda: iniciar_seguro(atras))),
            ("No lo tomaría", lambda: rama_rechazo_inicial(lambda: iniciar_seguro(atras))),
            (texto_info_gastos, lambda: rama_gastos(lambda: iniciar_seguro(atras)))
        ]
        cambiar_pantalla(texto, opciones, "Inicio del Simulador", "indicar.png", atras)
    
    def rama_rechazo_inicial(atras=None):
        texto = "Si el negocio sufre algún tipo de daño, deberás realizar una nueva inversión.\n\n¿Mantienes tu decisión o prefieres conocer más sobre los seguro antes de tomar una decisión?"
        texto_info_gastos = "Prefiero conocer más sobre las ganancias y gastos del negocio antes de tomar una decisión"
        
        opciones = [
            ("Conservo mi decisión, no tomaría un seguro", lambda: finalizar_simulacion("Ninguno")),
            (texto_info_gastos, lambda: rama_gastos(lambda: rama_rechazo_inicial(atras)))
        ]
        cambiar_pantalla(texto, opciones, "Rama de Rechazo de Seguro", "rechazo.png", atras)
    
    def rama_gastos(atras=None):
        texto = "--- INFORMACIÓN DE GASTOS ---\n\nLos gastos mensuales del local(arriendo, pago de servicios y otros) equivalen a $450.000\n\nTu inversión inicial para instalar y habilitar el negocio fue de $3.000.000.\n\nEl negocio proyecta una ganancia neta (lo que queda después de pagar los gastos) con un promedio mensual de $900.000.\n\n¿Tomarías el seguro?"
        texto_info_ofrecen = "No, necesito más información sobre lo que ofrecen los seguros antes de tomar una decisión"
        
        opciones = [
            # A PARTIR DE AQUÍ, LA LLAVE ESTÁ EN False
            ("Sí, lo tomaría", lambda: rama_aceptacion_base(rama_ofrecen, texto_info_ofrecen, False, lambda: rama_gastos(atras))),
            (texto_info_ofrecen, lambda: rama_ofrecen(lambda: rama_gastos(atras))),
            ("No tomaría un seguro", lambda: finalizar_simulacion("Ninguno"))
        ]
        cambiar_pantalla(texto, opciones, "Rama de Información de Gastos", "lista.png", atras)

    def rama_ofrecen(atras=None):
        texto = "--- INFORMACIÓN DE COBERTURA ---\n\nLa compañía ofrece dos tipos de seguros\n\n• Seguro Full: Prima mensual de $90.000. Cubre pérdida total por daños en la infraestructura del local y, además, daños o pérdidas de las mercancías, por conceptos de robo o siniestros.\n\n• Seguro Parcial: Prima mensual de $40.000. Cubre pérdida por daños en la infraestructura o bien daños o pérdidas en las mercancías, por concepto de robos o siniestros, con un tope máximo de $2.000.000.\n\n¿Tomarías alguno de los seguros?"
        texto_info_riesgos = "No, necesito información sobre los riesgos a los que está expuesto el negocio antes de tomar una decisión"
        
        opciones = [
            ("Sí, tomaría alguno", lambda: rama_aceptacion_base(rama_riesgos, texto_info_riesgos, False, lambda: rama_ofrecen(atras))),
            (texto_info_riesgos, lambda: rama_riesgos(lambda: rama_ofrecen(atras))),
            ("No tomaría un seguro", lambda: finalizar_simulacion("Ninguno"))
        ]
        cambiar_pantalla(texto, opciones, "Rama Información de Seguros", "lista.png", atras)
    
    def rama_riesgos(atras=None):
        texto = "--- INFORMACIÓN DE RIESGOS ---\n\nEn el sector donde estará el local comercial de tu futuro negocio, se sabe que:\n\n• Se reporta una tasa promedio mensual de 20% de robos menores.\n\n• Se reporta una tasa promedio mensual de 10% de robos mayores.\n\n• Se reporta una tasa promedio anual de 5% de siniestros catastróficos (incendios, inundaciones u otros)\n\n¿Tomarías el seguro?"
        texto_info_costos = "No, necesito más información sobre los costos si sufro un robo o un siniestro antes de tomar una decisión"
        
        opciones = [
            ("Sí, tomaría alguno", lambda: rama_aceptacion_base(rama_costos, texto_info_costos, False, lambda: rama_riesgos(atras))),
            (texto_info_costos, lambda: rama_costos(lambda: rama_riesgos(atras))),
            ("No tomaría un seguro", lambda: finalizar_simulacion("Ninguno"))
        ]
        cambiar_pantalla(texto, opciones, "Rama Información de Riesgos", "lista.png", atras)

    def rama_costos(atras=None):
        texto = "--- INFORMACIÓN DE COSTOS POR ROBO O SINIESTRO ---\n\nSegún registros de las autoridades locales, se sabe que:\n\n• Se reporta un costo promedio de $600.000 por sufrir robos menores.\n\n• Se reporta un costo promedio de $3.000.000 por sufrir robos mayores.\n\n• Se reporta que al sufrir un siniestro catastrófico (incendios, inundaciones u otros) la pérdida de tu patrimonio es total y para seguir con tu negocio se debe comenzar desde cero.\n\n¿Tomarías el seguro?"
        
        opciones = [
            ("Sí, tomaría un seguro", lambda: rama_aceptacion_base(None, None, False, lambda: rama_costos(atras))),
            ("No tomaría un seguro", lambda: finalizar_simulacion("Ninguno"))
        ]
        cambiar_pantalla(texto, opciones, "Rama Información de Costos", "lista.png", atras)
    
    def mostrar_proyeccion_5_años():
        page.controls.clear()

        page.add(componente_npc("¡Lo lograste! Revisa el resumen de tus decisiones y abre tu proyección final.", "idea.png"))
        page.add(ft.Divider(height=10, color="transparent"))

        page.add(ft.Text("📊 RESULTADOS Y TRAZABILIDAD", size=22, weight="bold", color=COLOR_AZUL_UCM, text_align=ft.TextAlign.CENTER))
        page.add(ft.Divider(height=20, color="transparent"))

        tipo_seguro = page.session.store.get("seguro_final")

        links_codap = {
            "Full" : "https://codap.concord.org/app/?v=3#shared=https%3A%2F%2Fcfm-shared.concord.org%2F2pV6PIAYZreunjfoUHpl%2Ffile.json",
            "Parcial" : "https://codap.concord.org/app/?v=3#shared=https%3A%2F%2Fcfm-shared.concord.org%2FBefRG9RYEnnlUaNrGMVv%2Ffile.json",
            "Ninguno" : "https://codap.concord.org/app/?v=3#shared=https%3A%2F%2Fcfm-shared.concord.org%2Fu8vVU8t95mpBEFu2IAXm%2Ffile.json"
        }

        enlace_seleccionado = links_codap.get(tipo_seguro, "")

        page.add(ft.Divider(height=20, color="transparent"))

        page.add(ft.Text("--- RESUMEN DE NAVEGACIÓN ---", weight="bold", color=COLOR_AZUL_UCM))

        rama_anterior = ""

        historial_actual = page.session.store.get("historial_decisiones")
        for rama, decision in historial_actual:
            if rama != rama_anterior:
                page.add(ft.Text(f"📍 {rama}", weight="bold", color=COLOR_CELESTE_UCM, size=14))
                rama_anterior = rama
            
            page.add(
                ft.Container(
                    content=ft.Text(f'↳ {decision}', size=13, color=ft.Colors.BLACK_87),
                    padding=ft.Padding.only(left=20, bottom=5)
                )
            )

        page.add(ft.Divider(height=20, color="transparent"))

        page.add(
            ft.Text(
                "💡 Importante: Al entrar al enlace, recuerda presionar el botón 'Comenzar' dentro de la simulación.", 
                color=ft.Colors.RED_700, 
                weight="bold",
                text_align=ft.TextAlign.CENTER
            )
        )

        boton_codap = ft.ElevatedButton(
            content=ft.Text("Ir a tu Proyección"),
            icon=ft.Icons.BAR_CHART,

            url=enlace_seleccionado,
            width=400
        )

        boton_siguiente = ft.ElevatedButton(
            content=ft.Text("Siguiente ➡"),
            style=ft.ButtonStyle(bgcolor=COLOR_CELESTE_UCM, color=ft.Colors.WHITE),
            on_click=lambda e: pantalla_reflexion_final(),
            width=400
        )

        page.add(boton_codap)
        page.add(ft.Divider(height=10, color="transparent"))
        page.add(boton_siguiente)

        page.update()

    def pantalla_reflexion_final():
        page.controls.clear()

        page.add(componente_npc(
            "Analizando tu proyección a 5 años... ¿qué conclusiones sacas para tu futuro?",
            "lectura.png"
        ))

        page.add(ft.Divider(height=10, color="transparent"))    

        page.add(ft.Text("Reflexión Final", size=22, weight="bold", color=COLOR_AZUL_UCM))
        page.add(ft.Text("Luego de la proyección obtenida, ¿mantendrías tu decisión? Explica tu respuesta.", size=16))

        campo_reflexion = ft.TextField(
            multiline=True,
            min_lines=5,
            border_color=COLOR_CELESTE_UCM,
            hint_text="Escribe tus conclusiones aquí...",
            width=400
        )

        def enviar_a_supabase(e):
            e.control.disabled = True
            e.control.content = ft.Text("Guardando...")

            anillo_carga = ft.Container(
                content=ft.ProgressRing(color=COLOR_CELESTE_UCM),
                alignment=ft.Alignment.CENTER,
                margin=ft.Margin.only(top=20)
            )
            page.add(anillo_carga)
            page.update()

            reflexion_estudiante = campo_reflexion.value

            nombre_recuperado = page.session.store.get("nombre_usuario")

            if not nombre_recuperado:
                nombre_recuperado = "Estudiante Sin Nombre"

            paquete_datos = {
                "id": page.session.store.get("id_sesion"),
                "nombre_estudiante": nombre_recuperado,
                "historial_decisiones": page.session.store.get("historial_decisiones"),
                "reflexion_final": reflexion_estudiante
            }

            try:
                respuesta = supabase.table("respuestas_simulador").insert(paquete_datos).execute()
                print("✅ Éxito al guardar:", respuesta.data)

                page.controls.clear()

                page.add(
                    componente_npc(
                        "¡Datos guardados con éxito! Ha sido un placer acompañarte en esta simulación.", 
                        "registro.png"  # Puedes usar saludo o celebracion, la que prefieras
                    )
                )
                page.add(ft.Divider(height=10, color="transparent"))

                page.add(ft.Text(f'¡Muchas gracias por participar, {page.session.store.get("nombre_usuario")}!', size=20, color=ft.Colors.GREEN_700))
                page.add(ft.Text("Tus respuestas han sido guardadas con éxito.", size=16))

                boton_reiniciar = ft.ElevatedButton(
                    content=ft.Text("🔄 Realizar otra simulación"),
                    style=ft.ButtonStyle(bgcolor=COLOR_AZUL_UCM, color=ft.Colors.WHITE),
                    on_click=lambda _: pantalla_seleccion_simulador(),
                    width=400
                )

                def cerrar_ventana(e):
                    page.controls.clear()

                    page.vertical_alignment = ft.MainAxisAlignment.CENTER
                    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
                    
                    # 3. Creamos la columna centrada: Texto arriba, NPC abajo
                    pantalla_despedida = ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "¡Simulación finalizada! Ya puedes devolver o bloquear este dispositivo.", 
                                    color=ft.Colors.BLACK87, 
                                    size=16, 
                                    text_align=ft.TextAlign.CENTER
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=20,
                                border_radius=20, 
                                border=ft.Border.all(2, COLOR_CELESTE_UCM),
                                width=350,
                                # Un pequeño margen inferior para que no quede pegado a la cabeza del robot
                                margin=ft.Margin.only(bottom=20) 
                            ),
                            
                            # El NPC ahora va debajo del contenedor
                            ft.Image(src="adios.png", width=300, height=300, fit="contain")
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0
                    )
                    
                    page.add(pantalla_despedida)
                    page.update()

                boton_cerrar = ft.ElevatedButton(
                    content= ft.Text("❌ Salir del Simulador"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
                    on_click=cerrar_ventana,
                    width=400
                )

                page.add(ft.Divider(height=20, color="transparent"))
                page.add(boton_reiniciar)
                page.add(ft.Divider(height=10, color="transparent"))
                page.add(boton_cerrar)
                page.update()

            except Exception as error:

                print("❌ Error al guardar en Supabase:", error)
        
        boton_enviar = ft.ElevatedButton(
            content=ft.Text("Finalizar y Guardar"),
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE),
            on_click=enviar_a_supabase, # <--- Al hacer clic, dispara la conexión
            width=400
            )
        page.add(campo_reflexion)
        page.add(ft.Divider(height=10, color="transparent"))
        page.add(boton_enviar)

        page.update()

    pantalla_bienvenida()
    
    
ft.app(target=main, assets_dir="assets")