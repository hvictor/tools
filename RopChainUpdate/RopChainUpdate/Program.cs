Console.Write("Exploit file: ");
var exploitFile = Console.ReadLine().TrimEnd('\r').TrimEnd('\n');

Console.Write("RP++ output file: ");
var gadgetsFile = Console.ReadLine().TrimEnd('\r').TrimEnd('\n');

Console.Write("DllBase variable in exploit code (e.g. 'dllBase'): ");
var dllBaseVar = Console.ReadLine().TrimEnd('\r').TrimEnd('\n');

var lines = File.ReadAllLines(exploitFile);
var gadgets = lines.Where(x => x.Contains("dllBase +")).ToList();

Dictionary<string, string> unique = new Dictionary<string, string>();

foreach (var g in gadgets)
{
    string offset = g.Split($"{dllBaseVar} +")[1].Split(")")[0].TrimStart();
    string instr = g.Split('#')[1].TrimStart();

    if (!instr.Contains("; ret") && !instr.Contains("; call") && !instr.Contains("; jmp"))
        continue;

    instr = instr.Substring(0, instr.IndexOf("; ret") + 4 + 1);
    
    if (!unique.ContainsKey(offset))
    {
        unique[offset] = instr;
    }
}

lines = File.ReadAllLines(gadgetsFile);

Dictionary<string, string> replacements = new Dictionary<string, string>();

foreach (var gadget in unique)
{
    var result = lines.FirstOrDefault(y => y.Contains($": {gadget.Value}"));
    if (result != null)
    {
        Console.WriteLine($"Planned Replacement: {gadget.Key}: {gadget.Value} ---> {result}");
        replacements[gadget.Key] = result.Split(":")[0];
    }
    else
    {
        Console.WriteLine($"(!) {gadget.Key}: {gadget.Value} not found in the new binary.");
    }
}

string exploitText = File.ReadAllText(exploitFile);

Console.Write("\n[>] Press Enter to apply Planned Replacements: ");
Console.ReadLine();

foreach (var r in replacements)
{
    Console.WriteLine($"[*] Replacing {r.Key} with {r.Value}");
    exploitText = exploitText.Replace(r.Key, r.Value);
}

var t = DateTime.Now;
var f = new FileInfo(exploitFile);
var updatedExploitFile = $"{f.DirectoryName}\\{t.ToString("yyyy-MM-dd_HHmmss")}-{f.Name}";
File.WriteAllText(updatedExploitFile, exploitText);
Console.WriteLine($"[+] Updated exploit file: {updatedExploitFile}");

Console.ReadLine();