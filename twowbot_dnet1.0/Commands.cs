using System.Threading.Tasks;
using Discord;
using Discord.Commands;
using Discord.WebSocket;

// Create a module with no prefix
public class Info : ModuleBase
{
	// ~say hello -> hello
	[Command("say"), Summary("Echos a message.")]
	public async Task Say([Remainder, Summary("The text to echo")] string echo)
	{
		// ReplyAsync is a method on ModuleBase
		await ReplyAsync(echo);
	}
}