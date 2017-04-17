using Discord;
using Discord.Commands;
using System.IO;

class Program
{
	static void Main(string[] args) => new Program().Start();

	private DiscordClient _client;

	public void Start()
	{
		_client = new DiscordClient();

		_client.UsingCommands(x => {
			x.PrefixChar = '+';
			x.HelpMode = HelpMode.Public;
		});

		char p = '+';

		_client.GetService<CommandService>().CreateGroup("do", cgb =>
			{
				cgb.CreateCommand("help")
					.Alias(new string[] { "pls-assist-me" })
					.Description("Tells you to not use this.")
					.Do(async e =>
						{
							await e.Channel.SendMessage($"The help command is actually `{p}help mini`. Yeah, I know, it's confusing.");
						});

				cgb.CreateCommand("create")
					.Alias(new string[] { "new", "make" })
					.Description("Creates a Mini TWOW.")
					.Parameter("GreetedPerson", ParameterType.Required)
					.Do(async e =>
						{
							await e.Channel.SendMessage($"this isn't even started yet scrub");
						});
			});

		_client.ExecuteAndWait(async () => {
			string token = File.ReadAllLines("token.txt")[0];
			await _client.Connect(token, TokenType.Bot);
		});
	}
}