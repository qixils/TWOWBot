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

		_client.GetService<CommandService>().CreateCommand("botok") //create command
		       .Alias("ping", "status") // add some aliases
               .Description("Checks if the bot is online.") //add description, it will be shown when +help is used
               .Do(async e => {
            await e.Channel.SendMessage($"bot is online \ud83d\udc4c");
               });

		_client.GetService<CommandService>().CreateCommand("create")
			   .Do(async e =>
			   {
			   });
			

		_client.GetService<CommandService>().CreateGroup("test", cgb =>
		{
	    	cgb.CreateCommand("data-save")
				.Description("Multi-server data test")
				.Parameter("data", ParameterType.Required)
				.Do(async e =>
				{
				    // e.GetArg("GreetedPerson");
				    await e.Channel.SendMessage($"data saved");
				});

			cgb.CreateCommand("data-load")
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