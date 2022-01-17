# written by AG buddy
import discord, csv, nest_asyncio
nest_asyncio.apply()


TOKEN = "OTEzODc2MTIzOTA4MjEwNzA4.YaE3dg.0hjzynxB1ga6xeFeNTN0wCvUcHI"

client = discord.Client()


def init_dict():
    try:
        infile = open("schedule.csv", "r", encoding="utf8")
        print("schedule.csv found! its a miracle!")
        D = {}
        reader = csv.reader(infile)
        for l in reader:
            if l[0] not in D:
                D[l[0]] = []
            L = [l[1], l[2], l[3], l[4]]
            print("L", L)
            D[l[0]].append(L)
            print("NEW {}: ".format(l[0]), D[l[0]])
        if len(D) == 0:
            print("schedule.csv found, but empty!")
        else:
            print("IMPORTED DICT FROM SCHEDULE.CSV:", D)
    except FileNotFoundError:
        print("No schedule.csv found. Initializing empty dictionary D.")
        
        print("writing to a new schedule.csv lol")
        outfile = open("schedule.csv", "w", encoding = "utf8")
        writer = csv.writer(outfile)
        writer.writerow(["LOL!"])
        outfile.close()
        
        D = {}
        
    try:
        donefile = open("donelist.csv", "r", encoding="utf8")
        print("donelist found!")
        dD = {}
        reader = csv.reader(donefile)
        for l in reader:
            if l[0] not in dD:
                dD[l[0]] = []
            L = [l[1], l[2], l[3], l[4]]
            dD[l[0]].append(L)
        if len(dD) == 0:
            print("this shit empty")
        else:
            print("doneDICT: ", dD)
    except FileNotFoundError:
        print("no donelist.csv found. Initializing empty dictionary dD.")
        print("writing a new donelist.csv")
        outfile_dl = open("donelist.csv", "w", encoding = "utf8")
        outfile_dl.close()
        
        dD = {}
        
    return D, dD

@client.event
async def on_ready():
    print("Logged in as: {0.user}".format(client))
    print("Hello world!")
    
@client.event
async def on_message(message):
    fusername = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{fusername}: {user_message} ({channel})")
    
    if message.author == client.user:
        return

    
    if user_message.lower() == "hello ag god":
        await message.channel.send("Hello AG Buddygod.")
        return
    elif user_message.lower() == "bye ag god":
        await message.channel.send("Goodbye AG Buddygod.")
        return
    elif user_message.lower() == "!write":
        await write_csv(D, dD)
        file = open("dd.txt", "rb")
        await message.channel.send("List sorted by due date:", file=discord.File(file, "dd.txt"))
        file.close()
    
    split_m = user_message.split(" ")
    if split_m[0] == "!add":
        await get_hw(split_m[1], message)
    elif split_m[0] == "!done":
        await done_hw(D, dD, split_m[1], message)
    
        
async def get_hw(k, message):
    await message.channel.send("Enter the assignment name / description.")
    assignment_message = await client.wait_for("message")
    assignment_name = str(assignment_message.content)
    await message.channel.send("When is the assignment due? Please send your message in this format: m/d, t")
    due_message = await client.wait_for("message")
    due = str(due_message.content)
    due = due.split(", ")
    date = due[0].split("/")
    await message.channel.send("Adding assignment to {}: {}".format(k, assignment_name))
    await message.channel.send("Due date: {}/{} at {}".format(date[0], date[1], due[1]))
    add_hw(D, k, assignment_name, due)
    
    
def add_hw(D, k, name, due):
    date = due[0].split("/")
    try:
        if D[k]:
            pass
    except KeyError:
        D[k] = []
    
    L = [date[0], date[1], name, due[1]]
    print("L", L)
    D[k].append(L)
    print("NEW {}: ".format(k), D[k])

async def done_hw(D, dD, k, message):
    await message.channel.send("Which assignment do you want to mark as finished?")
    ind = 1
    try:
        for hw in D[k]:
            print(hw)
            msg = "{}. {:>2s}/{:>2s}: {} at {}".format(str(ind), hw[0], hw[1], hw[2], hw[3])
            ind += 1
            await message.channel.send(msg)
        ind_message = await client.wait_for("message")
        user_ind = str(ind_message.content)
        if 0 < int(user_ind) <= ind:
            L = []
            for hw in D[k]:
                L.append(hw)
        deleteme = L[int(user_ind)-1]
        D[k].remove(deleteme)
        print("Updated DIC: ", D[k])
        try:
            if dD[k]:
                pass
        except KeyError:
            dD[k] = []
            
        dD[k].append(deleteme)
        print("Updated dD: ", dD)
        await message.channel.send("HW {} has been moved to the done list!".format(user_ind))
    except KeyError:
        await message.channel.send("Please enter a real class.")

async def write_csv(D, dD):
    sch = open("schedule.csv", "w", newline='', encoding="utf8")
    writer = csv.writer(sch)
    
    ML = []
    for c in D:
        c_str = str(c)
        for l in D[c]:
            if l[0] == c_str:
                pass
            else:
                print("l before", l)
                l.insert(0, c_str)
                print("l after", l)
            ML.append(l)
    ML = sorted(ML, key = lambda x: (x[0], x[1], x[2]))
    for l in ML:
        writer.writerow(l)
    sch.close()
    
    ## schedule for due date, sorting only by month/day
    sch_dd = open("schedule_dd.csv", "w", newline='', encoding="utf8")
    writer = csv.writer(sch_dd)
    ML = sorted(ML, key = lambda x: (x[1], x[2]))
    print(ML)
    for l in ML:
        writer.writerow(l)
    sch_dd.close()
    
    txt = open("dd.txt", "w")
    for l in ML:
        text = "{:>2s}/{:>2s}: {:>7s}: {} at {}\n".format(l[1], l[2], l[0], l[3], l[4])
        txt.write(text)
    txt.close()
    
    ## done csv
    done = open("donelist.csv", "w", newline='', encoding="utf8")
    writer = csv.writer(done)
    DL = []
    for c in dD:
        c_str = str(c)
        for l in dD[c]:
            if l[0] == c_str:
                pass
            else:
                print("l before", l)
                l.insert(0, c_str)
                print("l after", l)
            DL.append(l)
    DL = sorted(DL, key = lambda x: (x[0], x[1], x[2]))
    for l in DL:
        writer.writerow(l)
    done.close()

    
    
    
        

D, dD = init_dict()
client.run(TOKEN)