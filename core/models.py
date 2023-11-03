from dataclasses import dataclass

@dataclass
class Contact:
    t_name: str
    t_phone: str
    t_link: str
    name: str = None
    mail: str = None
    work_phone: str = None
    engineer: bool = False
    def to_dict(self):
        payload = self.__dict__
        return payload
    
class User:
    def __init__(self, uid, contact: Contact):
        self._uid = uid
        self.contact = contact
        self.is_admin = False
        self.work_load = 0

    @property
    def uid(self):
        return self._uid

    def change_role(self, is_admin=False):
        self.is_admin = is_admin

    def to_dict(self):
        contact = self.contact
        if type(contact) != dict:
            contact = self.contact.to_dict()
        payload = self
        payload.contact = contact
        return payload.__dict__
    
    def to_pretty(self):
        return f"""🔗 {self.contact.t_link or 'Анонимный контакт'}
👤 {self.contact.t_name} {self.contact.name or ''}
📞 Телеграм {self.contact.t_phone or '🚫'} 
☎️ Рабочий {self.contact.work_phone or '🚫'} 
📬 {self.contact.mail or '🚫'}
{'👨‍🔧 Инженер' if self.contact.engineer else '👨‍💻 Айти-Специалист'}
""" 

def check_contact(message):
    phone = None
    link = None
    if message.contact:
        phone = message.contact.phone_number
    if message.chat.username:
        link = f"@{message.chat.username}"
    return {
        "phone": phone,
        "link": link
    }

def user_build_from_message(message) -> User:
    data = check_contact(message)
    user = User(
        message.chat.id, 
        Contact(
            t_name=message.chat.full_name,
            t_phone=data["phone"],
            t_link=data["link"]
    ))
    return user

def user_build_from_dict(data: dict): # TODO
    contact_dict = data.get('contact')
    contact = ...
    user = ...
    user.contact = contact
    return user