import pygame

colors = {'white': (255, 255, 255),
          'black': (0, 0, 0),
          'light_blue': (41, 182, 246),
          'dark_blue': (21, 101, 192),
          'sign_in': (44, 101, 144),
          'light_red': (219, 76, 76),
          'coins': (253, 216, 53),
          'level': (0, 200, 83),
          'jenny': (197, 53, 74),
          'jon': (61, 139, 201),
          'charles': (225, 189, 80)}

pygame.font.init()
fonts = {'Small': pygame.font.SysFont('coolveticacondensedrgregular', 19),
         'Little': pygame.font.SysFont('coolveticacondensedrgregular', 22),
         'Regular': pygame.font.SysFont('coolveticacondensedrgregular', 28),
         'Medium': pygame.font.SysFont('coolveticacondensedrgregular', 31),
         'Large': pygame.font.SysFont('coolveticacondensedrgregular', 72),
         'Big': pygame.font.SysFont('coolveticacondensedrgregular', 100),
         'Title': pygame.font.SysFont('coolveticacondensedrgregular', 60),
         'Speech Balloon': pygame.font.SysFont('coolveticacondensedrgregular', 34),
         'Compressed': pygame.font.SysFont('coolveticacompressedrgregular', 40),
         'Username': pygame.font.SysFont('coolveticacondensedrgregular', 24),
         'NPC': pygame.font.SysFont('coolveticacondensedrgregular', 28)}

jon_missions = [[[100, 'Welcome to Volantis!',
                  "Hey, I'm Jon, one of the agents here in Volantis. As a diver, I like to be here in the beach, but I"
                  " heard that there is a secret room under the sea. Can you help me find it?",
                  100, '0', 20],
                 [101, 'Go for a walk',
                  "After you discovered the submarine room, it's time to see all of the rooms in Volantis!",
                  100, '0', 20],
                 [102, 'Teleportation',
                  "Another way of moving in Volantis is teleprorting! So, why not try it?",
                  100, '0', 20]],
                [[110, 'Make friends',
                  "For me, friends are the main part of Volantis. You can chat, play and even trade items together!"
                  " Let's see if you can be with another 2 players in the same room.",
                  200, '0', 30],
                 [111, 'More friends, more fun',
                  "You were 3 players in the same room, but can you do it with 5?",
                  250, '0', 40],
                 [112, 'So many friends!',
                  "Ok, this is the last one! 10 players in one room and I promise that it will pay off for you!",
                  500, '51', 100]],
                [[120, 'Chat',
                  "You can chat with other players using the chat box. Try to say something!",
                  50, '0', 10]]]

jenny_missions = [[[200, "Hi, it's Jenny!",
                    "My name is Jenny, and I am an agent in Volantis. I'm a forester, so you can always find me here in"
                    " the forest! Wait, you can't be here without sun protection! Go to the market and buy a"
                    " Summer Hat!",
                    200, '0', 120],
                   [201, 'Hide in the nature',
                    "In addition to the hat, you must change your body color to perfectly hide in the forest! Go to the"
                    " market and buy Green body color! Don't worry, I'll give you the money back!",
                    300, '0', 1000],
                   [202, 'Final step',
                    "Now, the last thing you need is to get a Camo Shirt! I know that it's a rare item, but I'm sure"
                    " you can find and get it!",
                    750, '0', 200]],
                  [[210, 'Trading',
                    "If you want to get a rare item, trading is the prefect solution for you! Just find another player"
                    " and give in return another item. Make a trade and you will get the reward!",
                    150, '0', 50]],
                  [[220, 'A lot of money!',
                    "With money, you can buy anything you want from the shop and play as many games as you want! So,"
                    " I will give you the next mission: Get 5000 coins and I will give you a great reward with..."
                    " more money!",
                    500, '0', 500]]]

charles_missions = [[[300, 'Agent Charles',
                      "Hi, I'm Charles, and I will be your agent in the plaza room. I like to be here in the city and"
                      " play games with other players. My favorite game is tic tac toe! I want you to accept this game"
                      " request of other player. Good luck!",
                      120, '0', 20],
                     [301, 'Win Tic-Tac-Toe',
                      "Now, you must win the game in order to complete the mission!",
                      180, '0', 30],
                     [302, 'Tournament',
                      "What about 5 games of tic tac toe? May the best win!",
                      300, '0', 80]],
                    [[310, 'Concentration Game',
                      "Know the concentration game? I really like to play it! Try to send some player a request to"
                      " join you for a game.",
                      100, '0', 20],
                     [311, 'Test your memory',
                      "Defeat your opponent in one concentration game and win the rewards!",
                      180, '0', 30],
                     [312, 'Practice makes perfect',
                      "In order to be a winner, you muse practice! Play 5 concentration games with other players.",
                      300, '0', 80]],
                    [[320, 'Level 3',
                      "Levels show your achievements and abillities here in Volantis. Earh XP and make it to level 3!",
                      200, '0', 60],
                     [321, 'Level 5',
                      "Your next mission it to be on level 5. I'm sure you can do this!",
                      400, '0', 120],
                     [322, 'Level 10',
                      "The last challenge is to go for level 10! I know that it's a hard task, but with time you will"
                      " that it's easier than you think!",
                      750, '0', 400]]]
