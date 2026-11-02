
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import java.io.Console;

public class PasswordCheck {
    public static void main(String[] args) {
        Console console = System.console();

        if (console == null) {
            System.out.println("Please run this program in a normal terminal.");
            return;
        }

        char[] input = console.readPassword("Enter a new admin password: ");
        String password = new String(input);

        if (password.length() < 12) {
            System.out.println("Use at least 12 characters. No changes made.");
            return;
        }

        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        System.out.println("BCrypt hash: " + encoder.encode(password));
    }
}
