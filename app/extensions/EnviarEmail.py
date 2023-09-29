import smtplib
from email.message import EmailMessage

class EnviaEmail:
    def enviarEmail(destinatario, senha):#Função para enviar E-mail
        try:
            endercoEmail = '' #E-mail que vai conectar no servidor
            senhaEmail = '' #Senha do e-mail
            
            msg = EmailMessage()
            msg['Subject'] = "Alteração de senha no GEF" #Assunto do E-mail
            msg["From"] = "" #Correspondente que vai aparcer no e-mail
            msg["To"] = destinatario #Pra quem vai enviar
            msg.set_type("text/html")
            msg.set_content("Alteração de senha no GEF") 
            #Mensagem
            htmlMsg = f"""
            <h3>Sua senha no sistema GEF foi alterada, favor utilizar a senha abaixo para entrar no sistema. Logo após altere-a</h3>
            <br>
            
            <p><strong>Senha:</strong> {senha}</p>
            <br><br>
            
            E-mail enviado automaticamnete. Não responder.<br>
            Obrigado!
            """
        
            msg.add_alternative(htmlMsg, subtype="html")
            
            with smtplib.SMTP_SSL('',) as smtp: #Abre o servidor executa as funções abaixo e fecha a conexão
                smtp.login(endercoEmail, senhaEmail) #Faz login no Servidor
                smtp.send_message(msg) #Envia o E-mail
            
            return True
        
        except:
            return False    
            