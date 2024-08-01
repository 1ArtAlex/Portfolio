import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class MainClass {
    private String dbPrem = "";
    private String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
    private String username;
    private String password;

    public static void main(String[] args) {
        MainClass mainClass = new MainClass();
        mainClass.showLogin();
    }

    public void showLogin() {
        JFrame loginFrame = new JFrame("Вход в систему управления базами данных");
        loginFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        loginFrame.setSize(400, 200);
        loginFrame.setLocationRelativeTo(null);

        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);

        JTextField usernameField = new JTextField(15);
        JPasswordField passwordField = new JPasswordField(15);

        JButton connectButton = new JButton("Подключиться");
        connectButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                username = usernameField.getText();
                password = new String(passwordField.getPassword());
                try {
                    Connection connection = DriverManager.getConnection(url, username, password);
                    DatabaseManager dbManager = new DatabaseManager(connection);
                    GUI gui = new GUI(dbManager, connection, username, password, dbPrem);
                    gui.createAndShowGUI();
                    loginFrame.dispose();
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(loginFrame, "Ошибка подключения: " + ex.getMessage());
                }
            }
        });

        gbc.gridx = 0;
        gbc.gridy = 0;
        panel.add(new JLabel("Логин:"), gbc);

        gbc.gridx = 1;
        gbc.gridy = 0;
        panel.add(usernameField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 1;
        panel.add(new JLabel("Пароль:"), gbc);

        gbc.gridx = 1;
        gbc.gridy = 1;
        panel.add(passwordField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(connectButton, gbc);

        loginFrame.add(panel);
        loginFrame.setVisible(true);
    }
}
