using Microsoft.Extensions.Hosting;

namespace Quix.Redshift.Writer
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var built = CreateHostBuilder(args).Build();
            Startup.AfterBuild(built.Services);
            built.Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureAppConfiguration((context, builder) => Startup.ConfigureAppConfiguration(context, builder, args))
                .ConfigureServices(Startup.ConfigureServices)
                .ConfigureLogging(Startup.ConfigureLogging);
    }
}