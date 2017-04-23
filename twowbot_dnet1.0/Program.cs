using Discord;
using Discord.WebSocket;
using Discord.Commands;
using System;
using System.Threading.Tasks;
using System.IO;
using System.Reflection;

namespace TWOWBot
{
	public class Program
	{
        private DiscordSocketClient client = new DiscordSocketClient();
        private CommandService commands = new CommandService();
        private DependencyMap map = new DependencyMap();

		public static void Main(string[] args)
			=> new Program().MainAsync().GetAwaiter().GetResult();

        public async Task MainAsync()
		{
	        client.Log += Log;
            await InstallCommands();

            string token = File.ReadAllLines("token.txt")[0];
	        await client.LoginAsync(TokenType.Bot, token);
	        await client.StartAsync();

	        // Block this task until the program is closed.
	        await Task.Delay(-1);
        }

        public async Task InstallCommands()
        {
            client.MessageReceived += HandleCommand;
            await commands.AddModulesAsync(Assembly.GetEntryAssembly());
        }
        public async Task HandleCommand(SocketMessage messageParam)
        {
        	// Don't process the command if it was a System Message
        	var message = messageParam as SocketUserMessage;
	        if (message == null) return;
	        // Create a number to track where the prefix ends and the command begins
        	int argPos = 0;
	        // Determine if the message is a command, based on if it starts with '!' or a mention prefix
        	if (!(message.HasStringPrefix("?mini", ref argPos) || message.HasMentionPrefix(client.CurrentUser, ref argPos))) return;
	        // Create a Command Context
	        var context = new CommandContext(client, message);
	        // Execute the command. (result does not indicate a return value, 
	        // rather an object stating if the command executed succesfully)
        	var result = await commands.ExecuteAsync(context, argPos, map);
	        if (!result.IsSuccess)
	        	await context.Channel.SendMessageAsync(result.ErrorReason);
	    }

		private Task Log(LogMessage msg)
		{
			Console.WriteLine(msg.ToString());
			return Task.CompletedTask;
		}
	}
}