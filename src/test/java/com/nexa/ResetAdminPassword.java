
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import java.io.Console;

public class ResetAdminPassword {
    public static void main(String[] args) {
        Console console = System.console();

        if (console == null) {
            System.out.println("Run this program directly in PowerShell.");
            return;
        }

        char[] input = console.readPassword("Enter a new admin password: ");
        String password = new String(input);

        if (password.length() < 12) {
            System.out.println("Password must be at least 12 characters.");
            return;
        }

        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        String hash = encoder.encode(password);

        System.out.println("Generated BCrypt hash:");
        System.out.println(hash);
    }
}
