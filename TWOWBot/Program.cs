using Discord;
using Discord.Commands;
using System.IO;
using System;
using System.Collections.Generic;
using System.Text;

class Program
{
	static void Main(string[] args) => new Program().Start();

	private DiscordClient _client;

	public void Start()
	{
		_client = new DiscordClient();

		_client.Log.Message += (s, e) => Console.WriteLine($"[{e.Severity} - {DateTime.UtcNow.Hour}:{DateTime.UtcNow.Minute}:{DateTime.UtcNow.Second}] {e.Source}: {e.Message}");

		_client.UsingCommands(x => {
			x.PrefixChar = '+';
			x.AllowMentionPrefix = true;
			x.HelpMode = HelpMode.Public;
		});

		// char p = '+';
		// var sepchar = Path.DirectorySeparatorChar;
		string topic = "Ready to play a Mini TWOW!";

		_client.GetService<CommandService>().CreateCommand("botok") //create command
		       .Alias("ping", "status") // add some aliases
               .Description("Checks if the bot is online.") //add description, it will be shown when +help is used
               .Do(async e => {
            await e.Channel.SendMessage($"bot is online \ud83d\udc4c");
               });

		_client.GetService<CommandService>().CreateCommand("prepare")
			   .Do(async e =>
			   {
				   User bot = e.Server.GetUser(_client.CurrentUser.Id);
				   if (bot.GetPermissions(e.Channel).ManageChannel)
				   {
					   if (e.User.GetPermissions(e.Channel).ManageChannel)
					   {
                           Save("data", e.Channel.Id.ToString(), e.Server.Id, 1);
					       Save("data", "0", e.Server.Id, 2);
                           //see README.md's dev notes for data.txt layout
                           await e.Channel.Edit(e.Channel.Name, $"{topic}\n{e.Channel.Topic}", e.Channel.Position);
                           await e.Channel.SendMessage($"This channel is now ready to play Mini TWOWs!");
					   }
				   }
				   else
				   {
					   await e.Channel.SendMessage($"Please give the bot permissions to manage the channel!");
				   }
			   });
			

		_client.GetService<CommandService>().CreateGroup("test", cgb =>
		{
	    	cgb.CreateCommand("save")
				.Description("Multi-server data test")
				.Parameter("data", ParameterType.Unparsed)
				.Do(async e =>
				{
					//Save("data", e.GetArg("data"), e.Server.Id, 1);
					//await e.Channel.SendMessage($"data saved");
					await e.Channel.SendMessage($"no");
				});

			cgb.CreateCommand("load")
				.Description("Multi-server data test")
				.Parameter("line", ParameterType.Required)
				.Do(async e =>
				{
					try
					{
      //                  int i = 0; // line number
					 //   bool success = int.TryParse(e.GetArg("line"), out i); // output line number to line number
						//if (success) // check if line number was parsed successfully
						//{
						//	string data = Load("data", e.Server.Id, i); // run Load with required data
						//	if (data != null) // check if operation was successful
						//		await e.Channel.SendMessage(data); // output line
						//	else // if it failed...
						//		await e.Channel.SendMessage("file/line didnt exist"); // ...then say it failed
						//}
						//else
						//{
						//    await e.Channel.SendMessage($"failed to parse input ({e.GetArg("line")})"); // input wasn't an int
						//}

						await e.Channel.SendMessage($"no");
					}
					catch (Exception error)
					{
					    await e.Channel.SendMessage($"error: {error.ToString()}");
					}
				});
		});

		_client.Ready += (s, e) =>
		{
			Console.WriteLine($"[{DateTime.UtcNow.Hour}:{DateTime.UtcNow.Minute}:{DateTime.UtcNow.Second}] Connected as {_client.CurrentUser.Name}#{_client.CurrentUser.Discriminator}");
		};

		_client.ExecuteAndWait(async () => {
			string token = File.ReadAllLines("token.txt")[0];
			await _client.Connect(token, TokenType.Bot);
		});
	}
	public void Save(string filename, string data, ulong server, int linenumber)
	{
        var sepchar = Path.DirectorySeparatorChar; // get operating system's directory seperation character
        var path = $"{Directory.GetCurrentDirectory() + sepchar + server.ToString() + sepchar}"; // get data save directory
        var datafile = $"{path + filename}data.txt"; // get config file
        Directory.CreateDirectory(path); // create directory

        StringBuilder newconfig = new StringBuilder(); // create empty "text file" in memory

		if (File.Exists(datafile)) // checks if data file exists
		{
			if (new FileInfo(datafile).Length >= 2) // checks if data file has data
			{
				string[] config = File.ReadAllLines(datafile); // read all lines of the text file
                int currentline = 1; // set current line in the text file
				foreach (String line in config)
				{
					if (currentline == linenumber) { newconfig.Append(data + Environment.NewLine); } // replace line 1 of data with custom stuff
					else { newconfig.Append(line + "\r\n"); } // add other lines to file
					currentline++; // increase line number
				}
			}

			else { newconfig.Append(data + Environment.NewLine); } // file has nothing so just add data to first line
		}

		else { newconfig.Append(data + Environment.NewLine); } // file doesn't exist so create it with input

		File.WriteAllText(datafile, newconfig.ToString()); // save changes to file
	}
	public string Load(string filename, ulong server, int line)
	{
		line -= 1;
		var sepchar = Path.DirectorySeparatorChar; // Grab the current operating system's seperation char. (eg. windows: \, linux: /)
        var path = $"{Directory.GetCurrentDirectory() + sepchar + server.ToString() + sepchar}"; // get directory of data file
        var datafile = $"{path + filename}.txt"; // get data file
        Directory.CreateDirectory(path); // create directory if it doesn't exist
		if (File.Exists(datafile)) // check if file exists
		{
		    var config = File.ReadAllLines(datafile); // read config
			if (!string.IsNullOrWhiteSpace(config[line]))
				return config[line]; // return line
			else
				return null;
		}
		else
		{
			return null; // can't load if file doesn't exist
		}
	}
}