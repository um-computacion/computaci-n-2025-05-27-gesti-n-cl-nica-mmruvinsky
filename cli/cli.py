import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.clinica import Clinica
    from src.paciente import Paciente
    from src.medico import Medico
    from src.especialidad import Especialidad
    from src.excepciones import *
except ImportError:
    print("❌ Error: No se pueden importar los módulos necesarios")
    print("Asegúrate de que la estructura de directorios sea correcta:")
    print("- src/clinica.py")
    print("- src/paciente.py")
    print("- src/medico.py")
    print("- src/especialidad.py")
    print("- src/excepciones.py")
    sys.exit(1)

class CLI:
    """Interfaz de consola para el sistema de gestión de clínica."""
    
    def __init__(self, clinica: Clinica):
        self.clinica = clinica
        self.ejecutando = True
    
    def limpiar_pantalla(self):
        """Limpia la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_header(self):
        print("=" * 50)
        print("    SISTEMA DE GESTIÓN DE CLÍNICA")
        print("=" * 50)
    
    def mostrar_menu_principal(self):
        print("\n📋 MENÚ PRINCIPAL")
        print("-" * 30)
        print("1. Gestión de Pacientes")
        print("2. Gestión de Médicos")
        print("3. Gestión de Turnos")
        print("4. Gestión de Recetas")
        print("5. Reportes")
        print("0. Salir")
    
    def solicitar_opcion(self, max_opcion: int) -> int:
        """Solicita una opción válida al usuario."""
        while True:
            try:
                opcion = int(input(f"Opción (0-{max_opcion}): "))
                if 0 <= opcion <= max_opcion:
                    return opcion
                print(f"Debe ser entre 0 y {max_opcion}")
            except:
                print("Solo números")
    
    # === GESTIÓN DE PACIENTES ===
    
    def menu_pacientes(self):
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            print("\n👤 GESTIÓN DE PACIENTES")
            print("-" * 30)
            print("1. Agregar Paciente")
            print("2. Listar Pacientes")
            print("3. Ver Historia Clínica")
            print("0. Volver")
            
            opcion = self.solicitar_opcion(3)
            
            if opcion == 1:
                self.agregar_paciente()
            elif opcion == 2:
                self.listar_pacientes()
            elif opcion == 3:
                self.ver_historia_clinica()
            elif opcion == 0:
                break
            
            self.pausar()
    
    def agregar_paciente(self):
        """Agrega un nuevo paciente."""
        print("\n➕ Agregar Paciente")
        print("-" * 20)
        
        try:
            nombre = input("Nombre y apellido: ").strip()
            dni = input("DNI: ").strip()
            fecha_nac = input("Fecha nacimiento (DD/MM/YYYY): ").strip()
            
            if not dni:
                print("❌ El DNI no puede estar vacío")
                return
            
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                return
            
            if not fecha_nac:
                print("❌ La fecha de nacimiento no puede estar vacía")
                return
            
            paciente = Paciente(nombre, dni, fecha_nac)
            self.clinica.agregar_paciente(paciente)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def listar_pacientes(self):
        """Lista todos los pacientes."""
        print("\n📋 Lista de Pacientes")
        print("-" * 30)
        
        pacientes = self.clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados")
            return
        
        for i, paciente in enumerate(pacientes, 1):
            print(f"{i}. {paciente.obtener_nombre()} - DNI: {paciente.obtener_dni()}")
    
    def ver_historia_clinica(self):
        """Muestra historia clínica de un paciente."""
        print("\n📄 Historia Clínica")
        print("-" * 20)
        
        dni = input("DNI del paciente: ").strip()
        historia = self.clinica.obtener_historia_clinica_por_DNI(dni)
        
        if historia:
            print(historia)
        else:
            print(f"❌ No se encontró historia para DNI: {dni}")
    
    # === GESTIÓN DE MÉDICOS ===
    
    def menu_medicos(self):
        """Menú de gestión de médicos."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            print("\n👨‍⚕️ GESTIÓN DE MÉDICOS")
            print("-" * 30)
            print("1. Agregar Médico")
            print("2. Listar Médicos")
            print("0. Volver")
            
            opcion = self.solicitar_opcion(2)
            
            if opcion == 1:
                self.agregar_medico()
            elif opcion == 2:
                self.listar_medicos()
            elif opcion == 0:
                break
            
            self.pausar()
    
    def agregar_medico(self):
        """Agrega un nuevo médico."""
        print("\n➕ Agregar Médico")
        print("-" * 20)
        
        try:
            nombre = input("Nombre: ").strip()
            matricula = input("Matrícula (MN#### o MP####): ").strip()
            
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                return
            
            if not matricula:
                print("❌ La matrícula no puede estar vacío")
                return
            
            especialidades = []
            print("\nEspecialidades (escribe 'fin' para terminar):")
            
            while True:
                tipo = input("Especialidad: ").strip()
                if tipo.lower() == 'fin':
                    break
                
                dias_input = input("Días (separados por comas): ").strip()
                dias = [d.strip() for d in dias_input.split(',')]
                
                if tipo and dias:
                    especialidad = Especialidad(tipo, dias)
                    especialidades.append(especialidad)
                    print(f"✅ {tipo} agregada")
            
            if not especialidades:
                print("❌ Debe tener al menos una especialidad")
                return
            
            medico = Medico(nombre, matricula, especialidades)
            self.clinica.agregar_medico(medico)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def listar_medicos(self):
        """Lista todos los médicos."""
        print("\n📋 Lista de Médicos")
        print("-" * 30)
        
        medicos = self.clinica.obtener_medicos()
        if not medicos:
            print("No hay médicos registrados")
            return
        
        for i, medico in enumerate(medicos, 1):
            print(f"{i}. {medico.obtener_nombre()} - Matrícula: {medico.obtener_matricula()}")
    
    # === GESTIÓN DE TURNOS ===
    
    def menu_turnos(self):
        """Menú de gestión de turnos."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            print("\n📅 GESTIÓN DE TURNOS")
            print("-" * 30)
            print("1. Agendar Turno")
            print("2. Listar Turnos")
            print("0. Volver")
            
            opcion = self.solicitar_opcion(2)
            
            if opcion == 1:
                self.agendar_turno()
            elif opcion == 2:
                self.listar_turnos()
            elif opcion == 0:
                break
            
            self.pausar()
    
    def agendar_turno(self):
        """Agenda un nuevo turno."""
        print("\n📅 Agendar Turno")
        print("-" * 20)
        
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matrícula del médico: ").strip()
            especialidad = input("Especialidad: ").strip()
            fecha_str = input("Fecha (DD/MM/YYYY): ").strip()
            hora_str = input("Hora (HH:MM): ").strip()
            
            fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M")
            
            resultado = self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            
            if not resultado:
                print("❌ No se pudo agendar el turno")
                
        except ValueError:
            print("❌ Formato de fecha/hora incorrecto")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def listar_turnos(self):
        """Lista todos los turnos."""
        print("\n📋 Lista de Turnos")
        print("-" * 30)
        
        turnos = self.clinica.obtener_turnos()
        if not turnos:
            print("No hay turnos registrados")
            return
    
    # === GESTIÓN DE RECETAS ===
    
    def menu_recetas(self):
        """Menú de gestión de recetas."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            print("\n💊 GESTIÓN DE RECETAS")
            print("-" * 30)
            print("1. Emitir Receta")
            print("2. Ver Recetas de Paciente")
            print("0. Volver")
            
            opcion = self.solicitar_opcion(2)
            
            if opcion == 1:
                self.emitir_receta()
            elif opcion == 2:
                self.ver_recetas_paciente()
            elif opcion == 0:
                break
            
            self.pausar()
    
    def emitir_receta(self):
        """Emite una nueva receta."""
        print("\n💊 Emitir Receta")
        print("-" * 20)
        
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matrícula del médico: ").strip()
            
            medicamentos = []
            print("\nMedicamentos (escribe 'fin' para terminar):")
            
            while True:
                med = input("Medicamento: ").strip()
                if med.lower() == 'fin':
                    break
                if med:
                    medicamentos.append(med)
                    print(f"✅ {med} agregado")
            
            if not medicamentos:
                print("❌ Debe agregar al menos un medicamento")
                return
            
            resultado = self.clinica.emitir_receta(dni, matricula, medicamentos)
            print(f"✅ {resultado}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ver_recetas_paciente(self):
        """Muestra recetas de un paciente."""
        print("\n💊 Recetas del Paciente")
        print("-" * 25)
        
        dni = input("DNI del paciente: ").strip()
        historia = self.clinica.obtener_historia_clinica_por_DNI(dni)
        
        if historia:
            recetas = historia.obtener_recetas()
            if recetas:
                for i, receta in enumerate(recetas, 1):
                    print(f"{i}. {receta}")
            else:
                print("❌ No hay recetas para este paciente")
        else:
            print(f"❌ No se encontró historia para DNI: {dni}")
    
    # === BUCLE PRINCIPAL ===
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación."""
        while self.ejecutando:
            try:
                self.limpiar_pantalla()
                self.mostrar_header()
                self.mostrar_menu_principal()
                
                opcion = self.solicitar_opcion(4)
                
                if opcion == 1:
                    self.menu_pacientes()
                elif opcion == 2:
                    self.menu_medicos()
                elif opcion == 3:
                    self.menu_turnos()
                elif opcion == 4:
                    self.menu_recetas()
                elif opcion == 0:
                    print("\n👋 ¡Hasta luego!")
                    self.ejecutando = False
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                self.ejecutando = False
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                self.pausar()

    def pausar(self):
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    try:
        clinica = Clinica({}, {}, [], {})
        cli = CLI(clinica)
        cli.ejecutar()
    except Exception as e:
        print(f"❌ Error al inicializar: {e}")