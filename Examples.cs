// Example usage of RakanGPT in a separate C# project
// Add this to your project to use RakanGPT as a library

using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace RakanGPT.Examples
{
    class ConsumerExample
    {
        private static readonly HttpClient client = new HttpClient();
        private const string BASE_URL = "http://localhost:5000";

        static async Task Main(string[] args)
        {
            Console.WriteLine("RakanGPT Consumer Example\n");

            // Example 1: Generate Essay
            await Example_GenerateEssay();

            // Example 2: Generate Email
            await Example_GenerateEmail();

            // Example 3: Check Grammar
            await Example_CheckGrammar();
        }

        static async Task Example_GenerateEssay()
        {
            Console.WriteLine("📚 Example 1: Generate Essay");
            Console.WriteLine("─────────────────────────────");

            var payload = new
            {
                topic = "The Future of Renewable Energy",
                style = "formal",
                length = "medium",
                check_grammar = true
            };

            try
            {
                var response = await client.PostAsync(
                    $"{BASE_URL}/generate/essay",
                    new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json")
                );

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(
                        await response.Content.ReadAsStringAsync()
                    );
                    
                    Console.WriteLine($"✅ Generated {result.word_count} word essay\n");
                    Console.WriteLine(result.essay.ToString().Substring(0, 300) + "...\n");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}\n");
            }
        }

        static async Task Example_GenerateEmail()
        {
            Console.WriteLine("✉️  Example 2: Generate Email");
            Console.WriteLine("──────────────────────────────");

            var payload = new
            {
                recipient = "Project Stakeholders",
                purpose = "Project completion notification",
                tone = "professional",
                key_points = new string[] 
                { 
                    "All deliverables completed on time",
                    "Team exceeded performance targets",
                    "Ready for production deployment"
                },
                check_grammar = true
            };

            try
            {
                var response = await client.PostAsync(
                    $"{BASE_URL}/generate/email",
                    new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json")
                );

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(
                        await response.Content.ReadAsStringAsync()
                    );
                    
                    Console.WriteLine("✅ Email generated successfully\n");
                    Console.WriteLine(result.email.ToString() + "\n");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}\n");
            }
        }

        static async Task Example_CheckGrammar()
        {
            Console.WriteLine("🔍 Example 3: Check Grammar");
            Console.WriteLine("─────────────────────────────");

            string textToCheck = "The student are very happy about there grades.";

            var payload = new { text = textToCheck };

            try
            {
                var response = await client.PostAsync(
                    $"{BASE_URL}/check-grammar",
                    new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json")
                );

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(
                        await response.Content.ReadAsStringAsync()
                    );
                    
                    Console.WriteLine($"Original: \"{textToCheck}\"");
                    Console.WriteLine($"Issues found: {result.issues_found}\n");
                    
                    if (result.issues_found > 0)
                    {
                        foreach (var issue in result.issues)
                        {
                            Console.WriteLine($"  • {issue.message}");
                            Console.WriteLine($"    Suggestion: {issue.suggestions[0]}\n");
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}\n");
            }
        }
    }
}
