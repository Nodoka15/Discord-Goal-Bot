import discord
from discord import Intents
from discord.ext import commands
import asyncio

#Data
user_name = []
temp_storage = {}
access_dict = {}
display_name = {}

#Necessary Methods:
def sign_up(name, dis_name):
    user_name.append(name)
    access_dict[name] = []
    temp_storage[name] = []
    display_name[name] = dis_name
    return(sign_page_success(dis_name))

def add_goal(goal, identifier):
    access_dict[identifier].append(goal)
    return(success_add_page(goal))

def remove_goal(number, identifier):
    user_goals = access_dict[identifier]
    if(number >=1 and number <= len(user_goals)):
        removed_goal = user_goals[number - 1]
        user_goals.pop(number - 1)
        return(removed_page(removed_goal))
    else:
         return(fail_page())

def edit_goal(number, new_goal, identifier):
    user_goals = access_dict[identifier]
    if (number >= 1 and number <= len(user_goals)):
        removed_goal = user_goals[number - 1]
        user_goals[number - 1] = new_goal
        return(edit_page(removed_goal, new_goal))
    else:
        return(fail_page())

def check_goal(list, form, identifier):
    user_goals = access_dict[identifier]
    storage = temp_storage[identifier]
    if form == 2:
        for goal in user_goals:
            storage.append(goal)
        access_dict[identifier] = []
    else:
        for index in list:
            if (index >= 1 and index <= len(user_goals)):
                storage.append(user_goals[index - 1])
                user_goals.pop(index - 1)
            else:
                return(fail_page())
    return(checked_page(identifier, form))


#Display Pages
#Sign Up Pages
def sign_page_ack():
    embed = discord.Embed(
        title="Sign Up!",
        color=discord.Color.yellow())
    embed.add_field(name="We have not detected you in our system.", value="To sign up, use the command !sign-up", inline=True)
    return embed

def sign_page_success(name):
    embed = discord.Embed(
        title="Congrats " + name + "!",
        color=discord.Color.green())
    embed.add_field(name=("You Are Now Signed Up!"), value="Start adding your goals by using the !add-goals command.", inline=True)
    return embed

#View Page
def view_goal(name):
    display = display_name[name]
    embed = discord.Embed(
        title="Weekly Goals for " + display,
        color=discord.Color.yellow())
    user_goals = access_dict[name]
    if(len(user_goals) == 0):
        embed.add_field(name="You Currently Have No Goals Set", value="Start setting goals by using the !add-goals command.", inline=False)
    else:
        for i in range(len(user_goals)):
            embed.add_field(name="", value=(str(i + 1)) + ": " + user_goals[i], inline=False)
    return embed

#Error/Cancels:
def fail_page():
    embed = discord.Embed(
        title="Fail",
        color=discord.Color.red())
    embed.add_field(name="", value="We've failed to complete your request.", inline=True)
    embed.set_footer(text="The issue might have been a typo or you took too long to respond. To retry, re-use the command you typed.")
    return embed

def cancel_page():
    embed = discord.Embed(
        title="Canceled",
        color=discord.Color.red())
    embed.add_field(name="", value="The request was canceled.", inline=True)
    embed.set_footer(text="To restart, re-use the command you have typed.")
    return embed

#Add Pages:
def add_page():
    embed = discord.Embed(
        title="Add New Goals",
        color=discord.Color.blue())
    embed.add_field(name="", value="Type a New Goal You Want to Add", inline=True)
    embed.set_footer(text='You can type "cancel" to stop.')
    return embed

def success_add_page(added_goal):
    embed = discord.Embed(
        title="Successful!",
        color=discord.Color.green())
    embed.add_field(name="Your New Goal Has Been Added", value=added_goal, inline=True)
    embed.set_footer(text='You can add another goal by entering it or type "Done" if you are finished.')
    return embed

def finished_add_page():
    embed = discord.Embed(
        title="Finished!",
        color=discord.Color.green())
    embed.add_field(name="", value="You're done with adding all your goals!", inline=True)
    embed.set_footer(text="You Can Check Them Using !weekly-goals")
    return embed

#Edit Page
def edit_add_page():
    embed = discord.Embed(
        title="Edit the Goal",
        color=discord.Color.blue())
    embed.add_field(name="", value="Type a New Goal You Want Instead", inline=True)
    embed.set_footer(text='You can type "cancel" to stop.')
    return embed
def edit_page(removed, added):
    embed = discord.Embed(
        title="Successful!",
        color=discord.Color.green())
    embed.add_field(name="The Goal You Chose Have Been Edited", value="", inline=False)
    embed.add_field(name="", value=("Removed: " + removed), inline=False)
    embed.add_field(name="", value=("Replaced With: " + added), inline=False)
    embed.set_footer(text="You Can Check it Using !weekly-goals")
    return embed

#Remove Page
def removed_page(removed_goal):
    embed = discord.Embed(
        title="Successful!",
        color=discord.Color.green())
    embed.add_field(name="The Goal Has Been Removed", value=removed_goal, inline=True)
    embed.set_footer(text="You Can Now Check Your List Using !weekly-goals")
    return embed

#Check-List Pages
def checked_page(name, form):
    completed = temp_storage[name]
    if form == 1:
        completed.reverse()
    embed = discord.Embed(
        title="Successful!",
        color=discord.Color.green())
    embed.add_field(name="The Goals You've Completed are Checked Off!", value="", inline=False)
    embed.add_field(name="Completed Goals:", value="", inline=False)
    for i in range(len(completed)):
        embed.add_field(name="", value=completed[i], inline=False)
    temp_storage[name] = []
    embed.set_footer(text="You Can Now Check Your Remaining Goals Using !weekly-goals")
    return embed

#Bot Setup
intents: Intents = Intents.default()
intents.message_content = True # NOQA

client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

#Handling Bot Startup
@client.event
async def on_ready():
    print("Bot is Online and Ready!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


#/help Command
@client.tree.command(name="help", description="Help Page")
async def embed(ctx):
    embed=discord.Embed(
    title="Helping Guide For Mr. Goals",
        description="Here are the available commands",
        color=discord.Color.green())
    embed.add_field(name="`!sign-up`", value="Sign into the system if you're using Mr. Goals for the first time!", inline=False)
    embed.add_field(name="`!weekly-goals`", value="View your goals for the week", inline=False)
    embed.add_field(name="`!add-goals`", value="Add a goal for the week", inline=False)
    embed.add_field(name="`!remove-goal`", value="Remove a goal for the week", inline=False)
    embed.add_field(name="`!edit-goal`", value="Edit a goal for the week", inline=False)
    embed.add_field(name="`!check-list`", value="Go through all your goals, check off ones you have finished.", inline=False)
    embed.add_field(name="`!remind` (Not Implemented Yet)", value="You will be able to set a reminder you want to your likings", inline=False)
    await ctx.response.send_message(embed=embed, ephemeral=True)

#!sign-up Command
@client.command(name="sign-up")
async def signup(ctx):
    name = ctx.author.name
    dis_name = ctx.author.display_name
    await ctx.send(embed=sign_up(name, dis_name))

#!weekly-goals Command
@client.command(name="weekly-goals")
async def weekly_goals(ctx):
    name = ctx.author.name

    if(name not in user_name):
        await ctx.send(embed=sign_page_ack())
    else:
        if (display_name[name] != ctx.author.display_name):
            display_name[name] = ctx.author.display_name

        embed = view_goal(name)
        embed.set_footer(text="Use: !add-goals to Add New Goals | !remove-goal to Remove a Goal | !edit-goal to Edit a Goal | !check-list to Check Off Goals You Have Completed")
        await ctx.send(embed=embed)


#!add-goal Command
@client.command(name="add-goals")
async def addgoal(ctx):
    name = ctx.author.name

    if(name not in user_name):
        await ctx.send(embed=sign_page_ack())
    else:
        if(display_name[name] != ctx.author.display_name):
            display_name[name] = ctx.author.display_name

        await ctx.send(embed=add_page())

        #Accept Message
        try:
            new_goal = await client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
        #Time Out
        except asyncio.TimeoutError:
            await ctx.send(embed=fail_page())

        else:
            #User Cancel
            if new_goal.content.lower() == "cancel":
                await ctx.send(embed=cancel_page())
            #Continue Code
            else:
                await ctx.send(embed=add_goal(new_goal.content, name))
                while True:
                    #Accept Message
                    try:
                        new_goal = await client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
                    #Time Out
                    except asyncio.TimeoutError:
                        fail_embed = fail_page()
                        fail_embed.add_field(name="", value="All of your previous tasks are saved however", inline=True)
                        await ctx.send(embed=fail_embed)
                        break
                    #User Finished
                    else:
                        if new_goal.content.lower() == "done":
                            await ctx.send(embed=finished_add_page())
                            break
                        #Continue Code
                        else:
                            await ctx.send(embed=add_goal(new_goal.content, name))



#!remove-goal Command
@client.command(name="remove-goal")
async def removegoal(ctx):
    name = ctx.author.name
    if(name not in user_name):
        await ctx.send(embed=sign_page_ack())
    else:
        if (display_name[name] != ctx.author.display_name):
            display_name[name] = ctx.author.display_name

        embed = view_goal(name)
        embed.set_footer(text='Enter the number corresponding to the goal that you want to REMOVE or type "cancel" to stop.')
        await ctx.send(embed=embed)

        #Accept Message
        try:
            number = await client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
        #Time Out
        except asyncio.TimeoutError:
            await ctx.send(embed=cancel_page())

        else:
            #User Cancel
            if number.content.lower() == "cancel":
                await ctx.send(embed=cancel_page())
            #Continue Code
            else:
                await ctx.send(embed=remove_goal(int(number.content), name))

#!edit-goal Command
@client.command(name="edit-goal")
async def editgoal(ctx):
    name = ctx.author.name
    if(name not in user_name):
        await ctx.send(embed=sign_page_ack())
    else:
        if (display_name[name] != ctx.author.display_name):
            display_name[name] = ctx.author.display_name

        embed = view_goal(name)
        embed.set_footer(text='Enter the number corresponding to the goal that you want to EDIT or type "cancel" to stop.')
        await ctx.send(embed=embed)

        #Accept Message
        try:
            number = await client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
        #Time Out
        except asyncio.TimeoutError:
            await ctx.send(embed=fail_page())
        else:
            #User Cancel
            if number.content.lower() == "cancel":
                await ctx.send(embed=cancel_page())
            #Continue Code
            else:
                await ctx.send(embed=edit_add_page())
                #Accept Message
                try:
                    new_goal = await client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
                #Time Out
                except asyncio.TimeoutError:
                    await ctx.send(embed=fail_page())

                else:
                    #User Cancel
                    if new_goal.content.lower() == "cancel":
                        await ctx.send(embed=cancel_page())
                    #Continue Code
                    else:
                        await ctx.send(embed=edit_goal(int(number.content), new_goal.content, name))

#!checklist Command
@client.command(name="check-list")
async def checklist(ctx):
    name = ctx.author.name
    if(name not in user_name):
        await ctx.send(embed=sign_page_ack())
    else:
        if (display_name[name] != ctx.author.display_name):
            display_name[name] = ctx.author.display_name

        embed = view_goal(name)
        embed.set_footer(text='Enter "all" to complete all goals or enter the number corresponding to the goal(s) that you\'ve completed. Make sure to separate by a space if it is multiple. Ex: 1 2 3...')
        await ctx.send(embed=embed)
        
        #Accept Message
        try:
            numbers = await client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
        #Time Out
        except asyncio.TimeoutError:
            await ctx.send(embed=fail_page())
        #User Cancel
        else:
            if numbers.content.lower() == "cancel":
                await ctx.send(embed=cancel_page())
            #Continue Code
            else:
                if numbers.content.lower() == "all":
                    form = 2
                    goal_finished = []
                else:
                    form = 1
                    goal_finished = (numbers.content).split(" ")
                    goal_finished = list(map(int, goal_finished))
                    goal_finished.sort(reverse = True)
                await ctx.send(embed=check_goal(goal_finished, form, name))




#Main Entry Point

#To run this bot, input your Discord Bot Token via Discord Developer Portal
"""
def main() -> None:
    client.run(token="Insert Your Discord Bot Token")

if __name__ == '__main__':
    main()
"""

