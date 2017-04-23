using Discord;
using Discord.Commands;
using System.IO;
using System;
using System.Collections.Generic;

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
				.Parameter("data", ParameterType.Required)
				.Do(async e =>
				{
					Console.WriteLine($"Starting data save test");
				var path = $"{Directory.GetCurrentDirectory() + sepchar + e.Server.Id.ToString() + sepchar}";
                var datafile = $"{path}data.txt";
				Console.WriteLine($"path: {path} \ndatafile: {datafile}");
                Directory.CreateDirectory(path);
			    File.Create(datafile);

					Console.WriteLine($"now going to edit data");
			    var config = File.ReadAllLines(datafile);
				config[0] = e.GetArg("data");
				File.WriteAllText(datafile, String.Join("\n", config));
				await e.Channel.SendMessage($"data saved");
				});

			cgb.CreateCommand("load")
				.Description("Multi-server data test")
				//.Parameter("data", ParameterType.Required)
				.Do(async e =>
				{
					string data = "unfinished";
				    await e.Channel.SendMessage($"saved data: {data}");
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