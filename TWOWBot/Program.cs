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
		var sepchar = Path.DirectorySeparatorChar;

		_client.GetService<CommandService>().CreateCommand("botok") //create command
		       .Alias("ping", "status") // add some aliases
               .Description("Checks if the bot is online.") //add description, it will be shown when +help is used
               .Do(async e => {
            await e.Channel.SendMessage($"bot is online \ud83d\udc4c");
               });

		_client.GetService<CommandService>().CreateCommand("create")
			   .Do(e =>
			   {
			   });
			

		_client.GetService<CommandService>().CreateGroup("test", cgb =>
		{
	    	cgb.CreateCommand("save")
				.Description("Multi-server data test")
				.Parameter("data", ParameterType.Unparsed)
				.Do(async e =>
				{
				// Console.WriteLine($"Starting data save test | input: {e.GetArg("data")}");
				var path = $"{Directory.GetCurrentDirectory() + sepchar + e.Server.Id.ToString() + sepchar}"; // get data save directory
				var datafile = $"{path}data.txt"; // get config file
				// Console.WriteLine($"path: {path} \ndatafile: {datafile}");
                Directory.CreateDirectory(path); // create directory
			    // File.Create(datafile); // create file

                StringBuilder newconfig = new StringBuilder(); // create empty "text file"

					if (File.Exists(datafile))
					{
					    // Console.WriteLine($"now going to edit data");
                        // Console.WriteLine($"file length: {new FileInfo(datafile).Length}");
				    	if (new FileInfo(datafile).Length >= 2)
					    {
					    	// Console.WriteLine($"file was detected as *not* empty");
					    	string[] config = File.ReadAllLines(datafile); // read all lines of the text file
                            // Console.WriteLine($"file read successful");
				    		int linenum = 1;
						    foreach (String line in config)
						    {
						    	if (linenum == 1) { newconfig.Append(e.GetArg("data") + Environment.NewLine); } // replace line 1 of data with custom stuff
						    	else { newconfig.Append(line + "\r\n"); } // add other lines to file
						    	linenum++; // increase line number
						    }
					    }

					    else { newconfig.Append(e.GetArg("data") + Environment.NewLine); }
					}

					else { newconfig.Append(e.GetArg("data") + Environment.NewLine); }
				// Console.WriteLine($"newconfig: {newconfig.ToString()}");

				File.WriteAllText(datafile, newconfig.ToString());
					// Console.WriteLine($"DATA SAVED WOO");
				await e.Channel.SendMessage($"data saved");
				});

			cgb.CreateCommand("load")
				.Description("Multi-server data test")
				//.Parameter("data", ParameterType.Required)
				.Do(async e =>
				{
                var path = $"{Directory.GetCurrentDirectory() + sepchar + e.Server.Id.ToString() + sepchar}";
                var datafile = $"{path}data.txt";
                Console.WriteLine($"path: {path} \ndatafile: {datafile}");
                Directory.CreateDirectory(path);
					if (File.Exists(datafile))
					{
						var config = File.ReadAllLines(datafile);
						await e.Channel.SendMessage($"line 1 data: {config[0]}");
					}
					else
					{
						await e.Channel.SendMessage($"file doesn't exist");
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
}