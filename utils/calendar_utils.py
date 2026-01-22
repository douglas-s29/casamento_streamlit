"""
Utilitários para gerar arquivos .ics (iCalendar)
para exportação de agendamentos para Google Calendar, Apple Calendar, Outlook, etc.
"""

from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import pytz

def gerar_ics_agendamento(agendamento):
    """
    Gera arquivo .ics para um agendamento específico
    
    Args:
        agendamento (dict): Dicionário com dados do agendamento
        
    Returns:
        bytes: Conteúdo do arquivo .ics
    """
    cal = Calendar()
    
    # Propriedades do calendário
    cal.add('prodid', '-//Gerenciador de Casamento//douglas-s29//PT-BR')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Casamento - Visitas')
    cal.add('x-wr-timezone', 'America/Sao_Paulo')
    cal.add('x-wr-caldesc', 'Agendamentos de visitas para o casamento')
    
    # Criar evento
    evento = Event()
    
    # Parsear data e hora
    try:
        if isinstance(agendamento['data'], str):
            data_agend = datetime.strptime(agendamento['data'], '%Y-%m-%d').date()
        else:
            data_agend = agendamento['data']
        
        if isinstance(agendamento['hora'], str):
            # Tentar diferentes formatos de hora
            try:
                hora_agend = datetime.strptime(agendamento['hora'], '%H:%M:%S').time()
            except ValueError:
                hora_agend = datetime.strptime(agendamento['hora'], '%H:%M').time()
        else:
            hora_agend = agendamento['hora']
    except Exception as e:
        raise ValueError(f"Erro ao parsear data/hora: {e}")
    
    # Timezone de São Paulo
    tz = pytz.timezone('America/Sao_Paulo')
    
    # Combinar data e hora
    inicio = tz.localize(datetime.combine(data_agend, hora_agend))
    fim = inicio + timedelta(hours=1)  # Duração padrão de 1 hora
    
    # UID único para o evento
    evento.add('uid', f"agendamento-{agendamento['id']}@casamento.douglas-s29.streamlit.app")
    
    # Título do evento
    titulo = f"{agendamento['categoria']} - {agendamento['local']}"
    evento.add('summary', titulo)
    
    # Datas
    evento.add('dtstart', inicio)
    evento.add('dtend', fim)
    evento.add('dtstamp', datetime.now(tz))
    evento.add('created', datetime.now(tz))
    evento.add('last-modified', datetime.now(tz))
    
    # Descrição detalhada
    descricao_partes = []
    descricao_partes.append(f"📅 Visita agendada: {agendamento['categoria']}")
    descricao_partes.append(f"🏢 Local: {agendamento['local']}")
    descricao_partes.append("")
    
    if agendamento.get('contato'):
        descricao_partes.append(f"👤 Contato: {agendamento['contato']}")
    if agendamento.get('telefone'):
        descricao_partes.append(f"📞 Telefone: {agendamento['telefone']}")
    if agendamento.get('endereco'):
        descricao_partes.append(f"📍 Endereço: {agendamento['endereco']}")
    
    descricao_partes.append("")
    
    if agendamento.get('observacao'):
        descricao_partes.append(f"📝 Observações:")
        descricao_partes.append(agendamento['observacao'])
        descricao_partes.append("")
    
    if agendamento.get('link'):
        descricao_partes.append(f"🔗 Link: {agendamento['link']}")
        descricao_partes.append("")
    
    descricao_partes.append(f"📊 Status: {agendamento.get('status', 'Agendado')}")
    descricao_partes.append("")
    descricao_partes.append("💍 Gerenciador de Casamento")
    descricao_partes.append("Criado em: douglas-s29/casamento_streamlit")
    
    evento.add('description', '\n'.join(descricao_partes))
    
    # Localização
    if agendamento.get('endereco'):
        evento.add('location', agendamento['endereco'])
    elif agendamento.get('local'):
        evento.add('location', agendamento['local'])
    
    # Status do evento
    status_evento = 'TENTATIVE'  # Default
    if 'Confirmado' in agendamento.get('status', '') or 'Concluído' in agendamento.get('status', ''):
        status_evento = 'CONFIRMED'
    elif 'Cancelado' in agendamento.get('status', ''):
        status_evento = 'CANCELLED'
    evento.add('status', status_evento)
    
    # Prioridade (Alta para visitas importantes)
    evento.add('priority', 5)  # 1=alta, 5=média, 9=baixa
    
    # Categoria
    categorias = [agendamento['categoria'].replace('🍰 ', '').replace('🏛️ ', '').replace('📸 ', '').strip(), 'Casamento', 'Visita']
    evento.add('categories', categorias)
    
    # Cor do evento (se o calendário suportar)
    evento.add('color', agendamento.get('cor', '#FF69B4'))
    
    # URL do evento (se tiver link)
    if agendamento.get('link'):
        evento.add('url', agendamento['link'])
    
    # Alarme/Lembrete (1 dia antes às 9h)
    alarme = Alarm()
    alarme.add('action', 'DISPLAY')
    alarme.add('description', f"Lembrete: {titulo}")
    alarme.add('trigger', timedelta(days=-1, hours=9))  # 1 dia antes às 9h
    evento.add_component(alarme)
    
    # Alarme adicional (2 horas antes)
    alarme2 = Alarm()
    alarme2.add('action', 'DISPLAY')
    alarme2.add('description', f"Lembrete: Visita em 2 horas - {agendamento['local']}")
    alarme2.add('trigger', timedelta(hours=-2))
    evento.add_component(alarme2)
    
    # Adicionar evento ao calendário
    cal.add_component(evento)
    
    return cal.to_ical()


def gerar_ics_multiplos_agendamentos(agendamentos, nome_arquivo="visitas"):
    """
    Gera arquivo .ics com múltiplos agendamentos
    
    Args:
        agendamentos (list): Lista de dicionários com agendamentos
        nome_arquivo (str): Nome base do arquivo
        
    Returns:
        bytes: Conteúdo do arquivo .ics
    """
    cal = Calendar()
    
    # Propriedades do calendário
    cal.add('prodid', '-//Gerenciador de Casamento//douglas-s29//PT-BR')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', f'Casamento - {nome_arquivo.title()}')
    cal.add('x-wr-timezone', 'America/Sao_Paulo')
    cal.add('x-wr-caldesc', f'Agendamentos de visitas para o casamento ({len(agendamentos)} eventos)')
    
    tz = pytz.timezone('America/Sao_Paulo')
    
    for agendamento in agendamentos:
        try:
            evento = Event()
            
            # Parsear data e hora
            if isinstance(agendamento['data'], str):
                data_agend = datetime.strptime(agendamento['data'], '%Y-%m-%d').date()
            else:
                data_agend = agendamento['data']
            
            if isinstance(agendamento['hora'], str):
                try:
                    hora_agend = datetime.strptime(agendamento['hora'], '%H:%M:%S').time()
                except ValueError:
                    hora_agend = datetime.strptime(agendamento['hora'], '%H:%M').time()
            else:
                hora_agend = agendamento['hora']
            
            # Combinar data e hora
            inicio = tz.localize(datetime.combine(data_agend, hora_agend))
            fim = inicio + timedelta(hours=1)
            
            # Propriedades do evento
            evento.add('uid', f"agendamento-{agendamento['id']}@casamento.douglas-s29.streamlit.app")
            evento.add('summary', f"{agendamento['categoria']} - {agendamento['local']}")
            evento.add('dtstart', inicio)
            evento.add('dtend', fim)
            evento.add('dtstamp', datetime.now(tz))
            evento.add('created', datetime.now(tz))
            
            # Descrição
            descricao = f"📅 Visita: {agendamento['categoria']}\n"
            descricao += f"🏢 Local: {agendamento['local']}\n\n"
            
            if agendamento.get('contato'):
                descricao += f"👤 Contato: {agendamento['contato']}\n"
            if agendamento.get('telefone'):
                descricao += f"📞 Telefone: {agendamento['telefone']}\n"
            if agendamento.get('observacao'):
                descricao += f"\n📝 Observações:\n{agendamento['observacao']}\n"
            if agendamento.get('link'):
                descricao += f"\n🔗 Link: {agendamento['link']}\n"
            
            descricao += f"\n📊 Status: {agendamento.get('status', 'Agendado')}\n"
            descricao += f"\n💍 Gerenciador de Casamento"
            
            evento.add('description', descricao)
            
            # Localização
            if agendamento.get('endereco'):
                evento.add('location', agendamento['endereco'])
            
            # Status
            status_evento = 'TENTATIVE'  # Default
            if 'Confirmado' in agendamento.get('status', '') or 'Concluído' in agendamento.get('status', ''):
                status_evento = 'CONFIRMED'
            elif 'Cancelado' in agendamento.get('status', ''):
                status_evento = 'CANCELLED'
            evento.add('status', status_evento)
            
            # Categoria
            categorias = [agendamento['categoria'].replace('🍰 ', '').replace('🏛️ ', '').replace('📸 ', '').strip(), 'Casamento']
            evento.add('categories', categorias)
            
            # Cor
            evento.add('color', agendamento.get('cor', '#FF69B4'))
            
            # URL
            if agendamento.get('link'):
                evento.add('url', agendamento['link'])
            
            # Alarme (1 dia antes)
            alarme = Alarm()
            alarme.add('action', 'DISPLAY')
            alarme.add('description', f"Lembrete: {agendamento['local']}")
            alarme.add('trigger', timedelta(days=-1, hours=9))
            evento.add_component(alarme)
            
            # Adicionar ao calendário
            cal.add_component(evento)
        
        except Exception as e:
            # Log do erro mas continua processando outros agendamentos
            print(f"Erro ao processar agendamento {agendamento.get('id', 'desconhecido')}: {str(e)}")
            continue
    
    return cal.to_ical()
