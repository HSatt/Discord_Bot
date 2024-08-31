import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View
from cogs.diyembed import diyembed
import random

strategies = {
  0: '',
  1: 'make sure to step back not to take Insta Kill ',
  2: 'make sure to step back not to take Insta Kill ',
  3: 'make sure to step back not to take Insta Kill ',
  4: 'make sure to step back not to take Insta Kill ',
  5: 'make sure to step back not to take Insta Kill ',
  6: "Save the spree for the end of the round, open Roller Coaster. # Never replace Pistol or Shotgun. Roll once only. Don't take puncher. What you need is a 3rd gun (Rainbow Rifle, Double Barrel Shotgun or Zombie Zapper - best weapon to get), as well as Lightning Rod Skill (heal skill is fine in the mean time) ",
  7: "Save the spree for the end of the round, open Roller Coaster. # Never replace Pistol or Shotgun. Roll once only. Don't take puncher. What you need is a 3rd gun (Rainbow Rifle, Double Barrel Shotgun or Zombie Zapper - best weapon to get), as well as Lightning Rod Skill (heal skill is fine in the mean time) ",
  8: 'Spread, kill zombies, nothing particular here, you can grow r10 slimes a bit, not important. ',
  9: 'Spread, kill zombies, nothing particular here, you can grow r10 slimes a bit, not important. ',
  10: 'Spread, kill zombies, nothing particular here, you can grow r10 slimes a bit, not important. ',
  11: 'Spread, kill zombies, nothing particular here, you can grow r10 slimes a bit, not important. ',
  12: 'Spread, kill zombies, nothing particular here, you can grow r10 slimes a bit, not important. ',
  13: 'Spread, kill zombies, nothing particular here, you can grow r10 slimes a bit, not important. ',
  14: 'Spread, kill zombies, nothing particular here, you can grow r10 slimes a bit, not important. ',
  15: 'Giant on last wave (when a few mobs left), not important to grow the slimes ',
  16: 'Grow slimes a bit. Open Ferris Wheel and ultimate Pistol and Shotgun. ',
  17: 'Grow slimes a bit. Open Ferris Wheel and ultimate Pistol and Shotgun. ',
  18: 'Camp at the Lucky Chest, grow slimes FULL size, for the scarce zombies that come, use pistol on them or shotgun aiming at the ground. ',
  19: "Open Bumper Cars, buy Fast Revive, Quick Fire and at least Extra Health 1. Get to Extra Health 3 asap (don't buy higher until Diamond Chestplate is acquired) ",
  20: '2 Giants (1-1) ',
  21: 'Only time you may take insta kill ',
  22: '2 Giants (1-1) ',
  23: 'Chest corner, grow slimes. ',
  24: '3 Giants (1-1-1) ',
  25: 'Mega Blob ',
  26: 'Chest corner, only slimes round, grow them FULL size.',
  27: 'nop',
  28: 'nop',
  29: "clowns 'n slimes stay close and keep moving to take less damage.",
  30: "4 Giants (1-1-2). Camp (near) chest corner unless it's specified otherwise.",
  31: 'nop',
  32: 'nop',
  33: 'You may grow slimes in perk corner preferably. ',
  34: 'You may grow slimes in perk corner preferably. ',
  35: 'Mega Magma ',
  36: '3 Giants (1-2), you can go middle for the first wave, there are clowns be careful, the first giant only spawn at the second wave ',
  37: '3 Giants (1-2) ',
  38: '3 Giants (1-2) ',
  39: '3 Giants (1-2), grow slimes. Aim at giants.',
  40: "4 Giants (2-2) + 1 o1 (The Old one) Wait the death of the o1 for get out of corner, if it does not come, it's probably stuck (often in Bumper Cars), stay in a corner or go on a stair (like on the refill ammo, at the edge of the block) and the o1 will be sort of stuck. Harder than r30-39, don't go too far from the chest or you'll make the entire team killed.",
  41: '4 Giants (2-2) ',
  42: '6 Giants (2-2-2) Now things start to get a little "spicy". Make sure to stay close to the chest. ',
  43: '6 Giants (2-2-2). Make sure to have 70+ ammo on the shotgun. Giga Slimes Round! Grow Slimes! FULL SIZE! Aim Giants! ',
  44: '9 Giants (3-3-3) ',
  45: '3 Giants (3). 2 old ones (2)! Go ultimate machine corner. ',
  46: '100% Golems. 1 Old One! Whole team camps in the Chest corner. ',
  47: '3 Giants (3). Make sure to have 70+ ammo on the shotgun. Giga Slimes Round! Grow Slimes! FULL SIZE! Aim Giants! ',
  48: 'Kill the creepers asap they do a lot of damage. 1 Old one! ',
  49: 'Clutch round, no giants, no o1, but tons of mobs and clowns. Dance for at least 20 seconds (dance = run among zombies while killing them asap), then go to Alt corner.',
  50: "4 Giants (2-2) From now on, mobs deal much more damage. The rounds you should be wary of in this block are 50, 55 and 58. Don't under-estimate. The new default corner is Ultimate Machine corner now.",
  51: '4 Giants (2-2), tons of Skeletons but they deal no damage. ',
  52: '4 Giants (2-2) CHEST CORNER. Giga Slimes Round! Grow Slimes! FULL SIZE! Aim Giants! ',
  53: '4 Giants (2-2). Tons of clowns ALT (better) OR ULT CORNER. Kill clowns and Giants asap! ',
  54: '4 Giants (2-2), now they are Rainbow giants! ALT (better) OR ULT CORNER. 2 o1 (1-1)! When the giants spawn, an o1 will arrive few seconds later, be careful! ',
  55: '5 Giants (1-1-1-1-1) ',
  56: 'Mega Blob, roll if you need and if someone does not have chestplate, let them solo this and the next round. ',
  57: 'Mega Magma. ',
  58: '6 Giants (3-3), 5 Old ones ALT (better) OR ULT CORNER',
  59: '13 o1! Just go on the ledge of a stair (you can spread 2-2) and kill them asap. ',
  60: 'Mini Space Blasters! A LOT! 2 o1! Everyone should have Diamond Chestplate and be set. Now focus on surviving and buy Extra Health when you can! The rounds 61-70, are the same as 71-80, 81-90 and 91-100 (except r89 and r99). When you get revived or when 2-3 people are down, block (right click) with your sword to take less damage. 1s or x1 means 61, 71, 81, 91 (same for 2s or x2 etc). 1 person buys Frozen Bullets, replacing Quick Fire. ',
  61: "Wolves and Magma cubes. Focus on wolves, kill them asap! Buy Quick Fire back (you'll understand for Round X0)",
  62: "Clown's party! Go near ALT corner. Wallshoot (if you know), just kill them asap (easiest rounds).",
  63: "Wolves and Creepers, don't let Creeper get close and kill the wolves.",
  64: "3rd Hardest rounds. 1-2 player go in the front and kill the Worms asap, after 10-15 seconds, go backwards while shooting. Time lightning well, no giants but still very hard if you do bad.",
  65: "GIANTS. 2nd Hardest rounds. The X5s are the easiest rounds to lose one as a few mistakes can quickly lead to a loss of the game. They aim at the giants and old ones to slow them down. Corner when giants arrive. Use lightning when there is a clutch at the corner.",
  66: "Magma Cubes, Creeper and Bombs. Buy Quick Fire back",
  67: "Fire lord zombies and Magma Cubes. Hard. Use lightning when a lot of zombies are near you.",
  68: "o1s! Golems, Worms and Bombs.",
  69: "Go to Perk corner, you will likely have a lot of bugged Zombies so be extremly careful near the end of the round. You will likely see more alive zombies than what is written in the scoreboard, that means some zombies are bugged or fake and can only be killed by melee. Identify them and kill them before starting the next round.",
  70: "Hardest rounds! Giants and o1! 1 player will focus the Iron Golems near the door, next to the window at the ultimate machine corner. 1 player will dance, loops in Park Entrance near the stone slabs (Ferris, Bumper, Roller, Ferris), makes sure they have the old ones on them. 1 player has Frozen Bullets and will focus the old ones on the dancer and will make sure to freeze the incoming Giants as well.",
  71: "Wolves and Magma cubes. Focus on wolves, kill them asap! Buy Quick Fire back (you'll understand for Round X0)",
  72: "Clown's party! Go near ALT corner. Wallshoot (if you know), just kill them asap (easiest rounds).",
  73: "Wolves and Creepers, don't let Creeper get close and kill the wolves.",
  74: "3rd Hardest rounds. 1-2 player go in the front and kill the Worms asap, after 10-15 seconds, go backwards while shooting. Time lightning well, no giants but still very hard if you do bad.",
  75: "GIANTS. 2nd Hardest rounds. The X5s are the easiest rounds to lose one as a few mistakes can quickly lead to a loss of the game. They aim at the giants and old ones to slow them down. Corner when giants arrive. Use lightning when there is a clutch at the corner.",
  76: "Magma Cubes, Creeper and Bombs. Buy Quick Fire back",
  77: "Fire lord zombies and Magma Cubes. Hard. Use lightning when a lot of zombies are near you.",
  78: "o1s! Golems, Worms and Bombs.",
  79: "Go to Perk corner, you will likely have a lot of bugged Zombies so be extremly careful near the end of the round. You will likely see more alive zombies than what is written in the scoreboard, that means some zombies are bugged or fake and can only be killed by melee. Identify them and kill them before starting the next round.",
  80: "Hardest rounds! Giants and o1! 1 player will focus the Iron Golems near the door, next to the window at the ultimate machine corner. 1 player will dance, loops in Park Entrance near the stone slabs (Ferris, Bumper, Roller, Ferris), makes sure they have the old ones on them. 1 player has Frozen Bullets and will focus the old ones on the dancer and will make sure to freeze the incoming Giants as well.",
  81: "Wolves and Magma cubes. Focus on wolves, kill them asap! Buy Quick Fire back (you'll understand for Round X0)",
  82: "Clown's party! Go near ALT corner. Wallshoot (if you know), just kill them asap (easiest rounds).",
  83: "Wolves and Creepers, don't let Creeper get close and kill the wolves.",
  84: "3rd Hardest rounds. 1-2 player go in the front and kill the Worms asap, after 10-15 seconds, go backwards while shooting. Time lightning well, no giants but still very hard if you do bad.",
  85: "GIANTS. 2nd Hardest rounds. The X5s are the easiest rounds to lose one as a few mistakes can quickly lead to a loss of the game. They aim at the giants and old ones to slow them down. Corner when giants arrive. Use lightning when there is a clutch at the corner.",
  86: "Magma Cubes, Creeper and Bombs. Buy Quick Fire back",
  87: "Fire lord zombies and Magma Cubes. Hard. Use lightning when a lot of zombies are near you.",
  88: "switch to alternative corner due to guardian zombies glitch",
  89: "Go to Perk corner, you will likely have a lot of bugged Zombies so be extremly careful near the end of the round. You will likely see more alive zombies than what is written in the scoreboard, that means some zombies are bugged or fake and can only be killed by melee. Identify them and kill them before starting the next round.",
  90: "Hardest rounds! Giants and o1! 1 player will focus the Iron Golems near the door, next to the window at the ultimate machine corner. 1 player will dance, loops in Park Entrance near the stone slabs (Ferris, Bumper, Roller, Ferris), makes sure they have the old ones on them. 1 player has Frozen Bullets and will focus the old ones on the dancer and will make sure to freeze the incoming Giants as well.",
  91: "Wolves and Magma cubes. Focus on wolves, kill them asap! Buy Quick Fire back (you'll understand for Round X0)",
  92: "Clown's party! Go near ALT corner. Wallshoot (if you know), just kill them asap (easiest rounds).",
  93: "Wolves and Creepers, don't let Creeper get close and kill the wolves.",
  94: "3rd Hardest rounds. 1-2 player go in the front and kill the Worms asap, after 10-15 seconds, go backwards while shooting. Time lightning well, no giants but still very hard if you do bad.",
  95: "GIANTS. 2nd Hardest rounds. The X5s are the easiest rounds to lose one as a few mistakes can quickly lead to a loss of the game. They aim at the giants and old ones to slow them down. Corner when giants arrive. Use lightning when there is a clutch at the corner.",
  96: "Magma Cubes, Creeper and Bombs. Buy Quick Fire back",
  97: "Fire lord zombies and Magma Cubes. Hard. Use lightning when a lot of zombies are near you.",
  98: "o1s! Golems, Worms and Bombs.",
  99: "switch to alternative corner due to guardian zombies glitch",
  100: "Hardest rounds! Giants and o1! 1 player will focus the Iron Golems near the door, next to the window at the ultimate machine corner. 1 player will dance, loops in Park Entrance near the stone slabs (Ferris, Bumper, Roller, Ferris), makes sure they have the old ones on them. 1 player has Frozen Bullets and will focus the old ones on the dancer and will make sure to freeze the incoming Giants as well.",
  101: "Buy Quick Fire back. Replace Zapper by Shotgun. Everyone goes at middle, aim high, headshot the boss: World Ender (500 hp). Use everything, lightning, double barrel, rainbow rifle, shotgun. You MUST kill it under 5 seconds or you lose (not hard) but make sure to use lightning and double barrel at least.",
  102: "Just a random o1 that runs but does not do any damage, the reason of these rounds existing is unknown but they are here.",
  103: "Just a random o1 that runs but does not do any damage, the reason of these rounds existing is unknown but they are here.",
  104: "Just a random o1 that runs but does not do any damage, the reason of these rounds existing is unknown but they are here.",
  105: "Just a random o1 that runs but does not do any damage, the reason of these rounds existing is unknown but they are here."
}

class MyView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
    async def left_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await E.left(self)
        await interaction.response.send_message("Left Button clicked!", ephemeral=True)
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
    async def right_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await E.right(self)
        await interaction.response.send_message("Right Button clicked!", ephemeral=True)

class E(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(aliases=["E"])
    async def e(self, ctx: Context) -> None:
        await ctx.reply("e")
    
    @commands.command(aliases=["mogus"])
    async def amogus(self, ctx: Context) -> None:
        view = MyView()
        global message
        
        message = await ctx.reply(embed=await diyembed.getembed(self, title='Play Among us now!', description='''"Among Us" is a multiplayer online game where players work together on a spaceship to complete tasks, 
                    but some are impostors trying to sabotage and eliminate the crew. Players must identify and vote out the impostors while impostors deceive and eliminate 
                    crew members without being caught. It's known for its social deduction gameplay.''', 
                    title_url='https://among.us', author_name='Among Us Promotion', author_url='https://among.us',
                    author_icon='https://i.imgur.com/YfUMLWc.png', thumbnail='https://i.imgur.com/YfUMLWc.png'
                    ), view=view)

    async def left(self):
        view = MyView()
        await message.edit(content="left", embed=None, view=view)

    async def right(self):
        view = MyView()
        await message.edit(content="right", embed=None, view=view)

    @commands.command(aliases=["rap, cap"])
    async def nap(self, ctx: Context) -> None:
        await ctx.reply(f"今日は**{random.randrange(1, 100)}**分昼寝しましょう！")

    @commands.command(aliases=["strat"])
    async def aa(self, ctx: Context, round: int) -> None:
        await ctx.reply(f'Round {round}: {strategies[round]}')

async def setup(bot: commands.Bot):
    await bot.add_cog(E(bot))
