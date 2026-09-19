using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace RakanGPT
{
    class Program
    {
        private static readonly HttpClient client = new HttpClient();
        private const string BASE_URL = "http://localhost:5000";

        static async Task Main(string[] args)
        {
            Console.WriteLine("╔══════════════════════════════════════╗");
            Console.WriteLine("║          Welcome to RakanGPT         ║");
            Console.WriteLine("║   AI Essay & Email Writer v1.0        ║");
            Console.WriteLine("╚══════════════════════════════════════╝\n");

            // Check if backend is running
            if (!await CheckBackendHealth())
            {
                Console.WriteLine("❌ Error: Python backend is not running on http://localhost:5000");
                Console.WriteLine("Please start the backend with: python backend.py");
                return;
            }

            bool running = true;
            while (running)
            {
                Console.WriteLine("\n📝 Main Menu:");
                Console.WriteLine("1. Generate Essay");
                Console.WriteLine("2. Generate Email");
                Console.WriteLine("3. Improve Text");
                Console.WriteLine("4. Check Grammar");
                Console.WriteLine("5. View Available Styles");
                Console.WriteLine("6. Exit");
                Console.Write("\nSelect option (1-6): ");

                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        await GenerateEssay();
                        break;
                    case "2":
                        await GenerateEmail();
                        break;
                    case "3":
                        await ImproveText();
                        break;
                    case "4":
                        await CheckGrammar();
                        break;
                    case "5":
                        await ShowStyles();
                        break;
                    case "6":
                        running = false;
                        Console.WriteLine("\n👋 Thank you for using RakanGPT!");
                        break;
                    default:
                        Console.WriteLine("❌ Invalid option. Please try again.");
                        break;
                }
            }
        }

        static async Task<bool> CheckBackendHealth()
        {
            try
            {
                var response = await client.GetAsync($"{BASE_URL}/health");
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        static async Task GenerateEssay()
        {
            Console.WriteLine("\n📚 Essay Generator");
            Console.WriteLine("─────────────────");

            Console.Write("Enter essay topic: ");
            string topic = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(topic))
            {
                Console.WriteLine("❌ Topic cannot be empty.");
                return;
            }

            Console.WriteLine("\nAvailable styles: formal, casual, creative, persuasive");
            Console.Write("Choose style (default: formal): ");
            string style = Console.ReadLine() ?? "formal";

            Console.WriteLine("\nEssay length: short (300-500), medium (600-900), long (1200-1500)");
            Console.Write("Choose length (default: medium): ");
            string length = Console.ReadLine() ?? "medium";

            Console.Write("Check grammar? (y/n, default: y): ");
            bool checkGrammar = Console.ReadLine()?.ToLower() != "n";

            try
            {
                Console.WriteLine("\n⏳ Generating essay...");

                var payload = new
                {
                    topic = topic,
                    style = style,
                    length = length,
                    check_grammar = checkGrammar
                };

                var response = await client.PostAsync(
                    $"{BASE_URL}/generate/essay",
                    new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json")
                );

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

                    Console.WriteLine("\n✅ Essay Generated Successfully!\n");
                    Console.WriteLine("═══════════════════════════════════════");
                    Console.WriteLine(result.essay);
                    Console.WriteLine("═══════════════════════════════════════\n");

                    Console.WriteLine($"📊 Word Count: {result.word_count}");
                    Console.WriteLine($"🎨 Style Used: {result.style_used}");

                    if (checkGrammar && result.grammar_issues.Count > 0)
                    {
                        Console.WriteLine($"\n⚠️  Grammar Issues Found: {result.grammar_issues.Count}");
                        for (int i = 0; i < Math.Min(5, result.grammar_issues.Count); i++)
                        {
                            var issue = result.grammar_issues[i];
                            Console.WriteLine($"  - {issue.message}");
                            if (issue.suggestions.Count > 0)
                                Console.WriteLine($"    Suggestion: {issue.suggestions[0]}");
                        }
                    }

                    Console.Write("\nSave essay to file? (y/n): ");
                    if (Console.ReadLine()?.ToLower() == "y")
                    {
                        string filename = $"essay_{DateTime.Now:yyyyMMdd_HHmmss}.txt";
                        System.IO.File.WriteAllText(filename, result.essay.ToString());
                        Console.WriteLine($"✅ Saved to: {filename}");
                    }
                }
                else
                {
                    Console.WriteLine($"❌ Error: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}");
            }
        }

        static async Task GenerateEmail()
        {
            Console.WriteLine("\n✉️  Email Generator");
            Console.WriteLine("──────────────────");

            Console.Write("Recipient name/title: ");
            string recipient = Console.ReadLine();

            Console.Write("Email purpose (request, inquiry, apology, thank you, etc.): ");
            string purpose = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(purpose))
            {
                Console.WriteLine("❌ Purpose cannot be empty.");
                return;
            }

            Console.WriteLine("\nAvailable tones: formal, casual, business, creative, persuasive");
            Console.Write("Choose tone (default: business): ");
            string tone = Console.ReadLine() ?? "business";

            Console.Write("Add key points? (y/n): ");
            List<string> keyPoints = new List<string>();
            if (Console.ReadLine()?.ToLower() == "y")
            {
                Console.WriteLine("Enter key points (press Enter twice to finish):");
                while (true)
                {
                    string point = Console.ReadLine();
                    if (string.IsNullOrWhiteSpace(point))
                        break;
                    keyPoints.Add(point);
                }
            }

            Console.Write("Check grammar? (y/n, default: y): ");
            bool checkGrammar = Console.ReadLine()?.ToLower() != "n";

            try
            {
                Console.WriteLine("\n⏳ Generating email...");

                var payload = new
                {
                    recipient = recipient,
                    purpose = purpose,
                    tone = tone,
                    key_points = keyPoints,
                    check_grammar = checkGrammar
                };

                var response = await client.PostAsync(
                    $"{BASE_URL}/generate/email",
                    new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json")
                );

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

                    Console.WriteLine("\n✅ Email Generated Successfully!\n");
                    Console.WriteLine("═══════════════════════════════════════");
                    Console.WriteLine(result.email);
                    Console.WriteLine("═══════════════════════════════════════\n");

                    Console.WriteLine($"🎨 Tone Used: {result.tone_used}");

                    if (checkGrammar && result.grammar_issues.Count > 0)
                    {
                        Console.WriteLine($"\n⚠️  Grammar Issues Found: {result.grammar_issues.Count}");
                        for (int i = 0; i < Math.Min(5, result.grammar_issues.Count); i++)
                        {
                            var issue = result.grammar_issues[i];
                            Console.WriteLine($"  - {issue.message}");
                        }
                    }

                    Console.Write("\nSave email to file? (y/n): ");
                    if (Console.ReadLine()?.ToLower() == "y")
                    {
                        string filename = $"email_{DateTime.Now:yyyyMMdd_HHmmss}.txt";
                        System.IO.File.WriteAllText(filename, result.email.ToString());
                        Console.WriteLine($"✅ Saved to: {filename}");
                    }
                }
                else
                {
                    Console.WriteLine($"❌ Error: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}");
            }
        }

        static async Task ImproveText()
        {
            Console.WriteLine("\n✨ Text Improvement");
            Console.WriteLine("──────────────────");

            Console.WriteLine("Paste your text (press Enter twice to finish):");
            StringBuilder textBuilder = new StringBuilder();
            string line;
            while ((line = Console.ReadLine()) != null)
            {
                if (string.IsNullOrEmpty(line) && textBuilder.Length > 0)
                    break;
                textBuilder.AppendLine(line);
            }

            string text = textBuilder.ToString().Trim();
            if (string.IsNullOrWhiteSpace(text))
            {
                Console.WriteLine("❌ Text cannot be empty.");
                return;
            }

            Console.WriteLine("\nImprovement types: clarity, grammar, style, conciseness, formal");
            Console.Write("Choose type (default: clarity): ");
            string type = Console.ReadLine() ?? "clarity";

            try
            {
                Console.WriteLine("\n⏳ Improving text...");

                var payload = new
                {
                    text = text,
                    improvement_type = type
                };

                var response = await client.PostAsync(
                    $"{BASE_URL}/improve",
                    new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json")
                );

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

                    Console.WriteLine("\n✅ Text Improved Successfully!\n");
                    Console.WriteLine("ORIGINAL:");
                    Console.WriteLine("─────────");
                    Console.WriteLine(result.original);
                    Console.WriteLine("\nIMPROVED:");
                    Console.WriteLine("────────");
                    Console.WriteLine(result.improved);
                    Console.WriteLine();
                }
                else
                {
                    Console.WriteLine($"❌ Error: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}");
            }
        }

        static async Task CheckGrammar()
        {
            Console.WriteLine("\n🔍 Grammar Checker");
            Console.WriteLine("─────────────────");

            Console.WriteLine("Paste your text (press Enter twice to finish):");
            StringBuilder textBuilder = new StringBuilder();
            string line;
            while ((line = Console.ReadLine()) != null)
            {
                if (string.IsNullOrEmpty(line) && textBuilder.Length > 0)
                    break;
                textBuilder.AppendLine(line);
            }

            string text = textBuilder.ToString().Trim();
            if (string.IsNullOrWhiteSpace(text))
            {
                Console.WriteLine("❌ Text cannot be empty.");
                return;
            }

            try
            {
                Console.WriteLine("\n⏳ Checking grammar...");

                var payload = new { text = text };

                var response = await client.PostAsync(
                    $"{BASE_URL}/check-grammar",
                    new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json")
                );

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

                    if (result.issues_found == 0)
                    {
                        Console.WriteLine("\n✅ No grammar issues found! Your text is perfect.");
                    }
                    else
                    {
                        Console.WriteLine($"\n⚠️  Found {result.issues_found} issue(s):\n");
                        for (int i = 0; i < Math.Min(10, result.issues.Count); i++)
                        {
                            var issue = result.issues[i];
                            Console.WriteLine($"{i + 1}. {issue.message}");
                            if (issue.suggestions.Count > 0)
                                Console.WriteLine($"   → Suggestion: {issue.suggestions[0]}");
                            Console.WriteLine();
                        }
                    }
                }
                else
                {
                    Console.WriteLine($"❌ Error: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}");
            }
        }

        static async Task ShowStyles()
        {
            try
            {
                var response = await client.GetAsync($"{BASE_URL}/styles");

                if (response.IsSuccessStatusCode)
                {
                    var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

                    Console.WriteLine("\n📚 Available Writing Styles\n");
                    Console.WriteLine("────────────────────────────");

                    var descriptions = result.descriptions;
                    foreach (var style in result.styles)
                    {
                        Console.WriteLine($"\n✓ {style}");
                        Console.WriteLine($"  → {descriptions[style.ToString()]}");
                    }
                    Console.WriteLine();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}");
            }
        }
    }
}
