import os
import time
import random
import sys

def clear_screen():
    os.system('clear')

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

class HorrorGame:
    def __init__(self):
        self.health = 100
        self.sanity = 100
        self.inventory = []
        self.current_room = "прихожая"
        self.game_over = False
        self.ghost_appear = False
        self.flashlight = True
        self.keys_found = 0
        
        self.rooms = {
            "прихожая": {
                "описание": "Ты стоишь в темной прихожей. Пахнет плесенью и пылью.",
                "выходы": ["гостиная", "кухня", "подвал"],
                "предмет": "ключ"
            },
            "гостиная": {
                "описание": "Старая гостиная с разбитой мебелью. Телевизор включен со статикой.",
                "выходы": ["прихожая", "спальня"],
                "предмет": "батарейка"
            },
            "кухня": {
                "описание": "Заброшенная кухня. На столе стоит гниющая еда.",
                "выходы": ["прихожая"],
                "предмет": "нож"
            },
            "спальня": {
                "описание": "Детская спальня. На кровати сидит старая кукла.",
                "выходы": ["гостиная"],
                "предмет": "дневник"
            },
            "подвал": {
                "описание": "Темный подвал. Слышны странные шепоты.",
                "выходы": ["прихожая", "тайная комната"],
                "предмет": "фонарь"
            },
            "тайная комната": {
                "описание": "Секретная комната. Здесь находится выход!",
                "выходы": ["подвал"],
                "предмет": "выход"
            }
        }

    def show_title(self):
        clear_screen()
        print("=" * 50)
        print("""
  ██████  ██████  ██   ██ ██████  ██████  
 ██      ██    ██ ██  ██  ██   ██ ██   ██ 
 ██      ██    ██ █████   ██████  ██████  
 ██      ██    ██ ██  ██  ██      ██   ██ 
  ██████  ██████  ██   ██ ██      ██   ██ 
                                          
        """)
        print("       ПРОКЛЯТЫЙ ДОМ")
        print("=" * 50)
        time.sleep(2)

    def show_status(self):
        print(f"\n❤️  Здоровье: {self.health}%")
        print(f"🧠 Рассудок: {self.sanity}%")
        print(f"🎒 Инвентарь: {', '.join(self.inventory) if self.inventory else 'пусто'}")
        print(f"📍 Комната: {self.current_room}")
        print("-" * 30)

    def random_event(self):
        event_chance = random.randint(1, 10)
        
        if event_chance <= 3:
            self.ghost_appear = True
            slow_print("\n👻 Ты слышишь шепот за спиной...")
            self.sanity -= 10
            time.sleep(2)
            
        elif event_chance <= 5:
            slow_print("\n💡 Фонарь мигает... Батарея садится!")
            self.flashlight = not random.choice([True, False])
            time.sleep(1)

    def move_to_room(self, room):
        if room in self.rooms[self.current_room]["выходы"]:
            self.current_room = room
            slow_print(f"\n🚶 Ты перешел в {room}...")
            
            room_item = self.rooms[room]["предмет"]
            if room_item not in self.inventory and room_item != "выход":
                slow_print(f"🔍 Ты нашел {room_item}!")
                self.inventory.append(room_item)
                self.keys_found += 1
                
            self.random_event()
            
            return True
        else:
            slow_print("\n❌ Нельзя пойти в эту комнату отсюда!")
            return False

    def use_item(self, item):
        if item in self.inventory:
            if item == "фонарь":
                self.flashlight = True
                slow_print("💡 Фонарь включен! Стало светлее.")
            elif item == "нож":
                slow_print("🔪 Ты взял нож в руки. Чувствуешь себя защищеннее.")
                self.health += 5
            elif item == "батарейка":
                slow_print("🔋 Ты поменял батарейки в фонаре.")
                self.flashlight = True
            elif item == "дневник":
                slow_print("📖 В дневнике написано: 'Он боится света...'")
        else:
            slow_print("❌ У тебя нет этого предмета!")

    def check_win_condition(self):
        if self.current_room == "тайная комната" and self.keys_found >= 3:
            slow_print("\n🎉 ПОБЕДА! Ты нашел все ключи и выбрался из дома!")
            slow_print("Ты выжил в этом кошмаре...")
            return True
        return False

    def check_game_over(self):
        if self.health <= 0:
            slow_print("\n💀 ТЫ УМЕР... Призраки забрали твою душу.")
            return True
        elif self.sanity <= 0:
            slow_print("\n😵 ТЫ СОШЕЛ С УМА... Дом поглотил твой разум.")
            return True
        return False

    def show_help(self):
        print("\n📖 КОМАНДЫ:")
        print("идти [комната] - перейти в другую комнату")
        print("использовать [предмет] - использовать предмет")
        print("статус - показать состояние")
        print("комнаты - показать доступные комнаты")
        print("выход - закончить игру")

    def play(self):
        self.show_title()
        
        slow_print("Ты просыпаешься в старом заброшенном доме...")
        slow_print("Нужно найти 3 ключа и выбраться через тайную комнату!")
        slow_print("Будь осторожен - дом полон призраков...")
        time.sleep(2)
        
        while not self.game_over:
            clear_screen()
            
            room_desc = self.rooms[self.current_room]["описание"]
            slow_print(f"\n{room_desc}")
            
            self.show_status()
            
            exits = self.rooms[self.current_room]["выходы"]
            slow_print(f"🚪 Выходы: {', '.join(exits)}")
            
            command = input("\n➡️  Что будешь делать? ").lower().strip()
            
            if command.startswith("идти "):
                room = command[5:]
                self.move_to_room(room)
                
            elif command.startswith("использовать "):
                item = command[13:]
                self.use_item(item)
                
            elif command == "статус":
                continue
                
            elif command == "комнаты":
                slow_print("\n🏠 Комнаты дома: " + ", ".join(self.rooms.keys()))
                
            elif command == "помощь":
                self.show_help()
                
            elif command == "выход":
                slow_print("🚪 Ты сдался... Дом поглотит тебя навсегда.")
                break
                
            else:
                slow_print("❌ Неизвестная команда. Напиши 'помощь' для списка команд.")
            
            input("\nНажми Enter чтобы продолжить...")
            
            if self.check_win_condition():
                break
                
            if self.check_game_over():
                break
            
            self.sanity -= random.randint(1, 3)
            if not self.flashlight:
                self.sanity -= 2

if __name__ == "__main__":
    try:
        game = HorrorGame()
        game.play()
    except KeyboardInterrupt:
        print("\n\n👋 Игра прервана. До свидания!")