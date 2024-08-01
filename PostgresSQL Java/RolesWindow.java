import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.Connection;
import java.sql.*;
import java.util.ArrayList;


public class RolesWindow {
    private Connection connection;

    public RolesWindow(Connection connection) {
        this.connection = connection;
    }

    public void createAndShowRolesWindow() {
        JFrame rolesFrame = new JFrame("Управление ролями");
        rolesFrame.setSize(400, 300);
        rolesFrame.setLayout(new BorderLayout());
        rolesFrame.setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(5, 1, 5, 5));

        // Кнопка "Просмотр ролей"
        JButton viewRolesButton = new JButton("Просмотр ролей");
        viewRolesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                RolesManager rolesManager = new RolesManager(connection);
                rolesManager.showAllRoles();
            }
        });

        // Кнопка "Добавить роль"
        JButton addRoleButton = new JButton("Добавить роль");
        addRoleButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JPanel inputPanel = new JPanel(new GridLayout(10, 2));
                JTextField usernameField = new JTextField();
                JPasswordField passwordField = new JPasswordField();
                JCheckBox createDeleteDBCheckBox = new JCheckBox("Создание/удаление базы данных");
                JCheckBox allowLoginCheckBox = new JCheckBox("Разрешен вход");
                JCheckBox superuserCheckBox = new JCheckBox("Superuser");
                JCheckBox createRolesCheckBox = new JCheckBox("Создание ролей");
                JCheckBox inheritCheckBox = new JCheckBox("Наследует права от родительских ролей");
                JCheckBox replicationCheckBox = new JCheckBox("Может создавать потоковую репликацию и резервные копии");
                JCheckBox bypassRLSCheckBox = new JCheckBox("Bypass RLS");

                inputPanel.add(new JLabel("Логин:"));
                inputPanel.add(usernameField);
                inputPanel.add(new JLabel("Пароль:"));
                inputPanel.add(passwordField);
                inputPanel.add(new JLabel("Права доступа:"));
                inputPanel.add(createDeleteDBCheckBox);
                inputPanel.add(new JLabel());
                inputPanel.add(allowLoginCheckBox);
                inputPanel.add(new JLabel());
                inputPanel.add(superuserCheckBox);
                inputPanel.add(new JLabel());
                inputPanel.add(createRolesCheckBox);
                inputPanel.add(new JLabel());
                inputPanel.add(inheritCheckBox);
                inputPanel.add(new JLabel());
                inputPanel.add(replicationCheckBox);
                inputPanel.add(new JLabel());
                inputPanel.add(bypassRLSCheckBox);

                int result = JOptionPane.showConfirmDialog(rolesFrame, inputPanel,
                        "Введите данные для новой роли", JOptionPane.OK_CANCEL_OPTION);

                if (result == JOptionPane.OK_OPTION) {
                    String username = usernameField.getText();
                    String password = new String(passwordField.getPassword());
                    boolean createDeleteDB = createDeleteDBCheckBox.isSelected();
                    boolean allowLogin = allowLoginCheckBox.isSelected();
                    boolean superuser = superuserCheckBox.isSelected();
                    boolean createRoles = createRolesCheckBox.isSelected();
                    boolean inherit = inheritCheckBox.isSelected();
                    boolean replication = replicationCheckBox.isSelected();
                    boolean bypassRLS = bypassRLSCheckBox.isSelected();

                    RolesManager rolesManager = new RolesManager(connection);
                    try {
                        rolesManager.addRole(username, password, createDeleteDB, allowLogin, superuser, createRoles, inherit, replication, bypassRLS); // добавление новой роли
                        JOptionPane.showMessageDialog(rolesFrame, "Роль \"" + username + "\" успешно создана");
                    } catch (SQLException ex) {
                        JOptionPane.showMessageDialog(rolesFrame, "Ошибка при добавлении роли: " + ex.getMessage());
                    }
                }
            }
        });

        // Кнопка "Удалить роли"
        JButton deleteRolesButton = new JButton("Удалить роли");
        deleteRolesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                RolesManager rolesManager = new RolesManager(connection);
                try {
                    ArrayList<String> roles = rolesManager.getRoles();

                    JPanel rolesPanel = new JPanel(new GridLayout(0, 1));
                    ArrayList<JCheckBox> checkBoxes = new ArrayList<>();

                    for (String role : roles) {
                        JCheckBox checkBox = new JCheckBox(role);
                        checkBoxes.add(checkBox);
                        rolesPanel.add(checkBox);
                    }

                    int result = JOptionPane.showConfirmDialog(null, rolesPanel,
                            "Выберите роли для удаления", JOptionPane.OK_CANCEL_OPTION);

                    if (result == JOptionPane.OK_OPTION) {
                        for (JCheckBox checkBox : checkBoxes) {
                            if (checkBox.isSelected()) {
                                String roleName = checkBox.getText();
                                rolesManager.deleteRole(roleName);
                            }
                        }
                        JOptionPane.showMessageDialog(null, "Роли успешно удалены");
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(null, "Ошибка при получении или удалении роли: " + ex.getMessage());
                }
            }
        });

        // Кнопка "Просмотр прав"
        JButton viewPermissionsButton = new JButton("Просмотр прав");
        viewPermissionsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                RolesManager rolesManager = new RolesManager(connection);
                try {
                    ArrayList<String> allRoles = rolesManager.getRoles();

                    JPanel selectRolePanel = new JPanel(new BorderLayout());
                    JComboBox<String> roleComboBox = new JComboBox<>(allRoles.toArray(new String[0]));
                    selectRolePanel.add(new JLabel("Выберите роль:"), BorderLayout.NORTH);
                    selectRolePanel.add(roleComboBox, BorderLayout.CENTER);

                    int result = JOptionPane.showConfirmDialog(rolesFrame, selectRolePanel,
                            "Выберите роль для просмотра прав", JOptionPane.OK_CANCEL_OPTION);

                    if (result == JOptionPane.OK_OPTION) {
                        String selectedRole = (String) roleComboBox.getSelectedItem();
                        String rolePrivileges = rolesManager.getRolePrivileges(selectedRole);

                        JOptionPane.showMessageDialog(rolesFrame, "Права для роли \"" + selectedRole + "\":\n\n" + rolePrivileges);
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(rolesFrame, "Ошибка при получении прав роли: " + ex.getMessage());
                }
            }
        });

        // Кнопка "Изменить права"
        JButton changePermissionsButton = new JButton("Изменить права");
        changePermissionsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                RolesManager rolesManager = new RolesManager(connection);
                try {
                    ArrayList<String> allRoles = rolesManager.getRoles();

                    JPanel selectRolePanel = new JPanel(new BorderLayout());
                    JComboBox<String> roleComboBox = new JComboBox<>(allRoles.toArray(new String[0]));
                    selectRolePanel.add(new JLabel("Выберите роль:"), BorderLayout.NORTH);
                    selectRolePanel.add(roleComboBox, BorderLayout.CENTER);

                    int result = JOptionPane.showConfirmDialog(rolesFrame, selectRolePanel,
                            "Выберите роль для изменения прав", JOptionPane.OK_CANCEL_OPTION);

                    if (result == JOptionPane.OK_OPTION) {
                        String selectedRole = (String) roleComboBox.getSelectedItem();

                        String rolePrivileges = rolesManager.getRolePrivileges(selectedRole);

                        JPanel inputPanel = new JPanel(new GridLayout(0, 1));
                        JTextField usernameField = new JTextField();
                        JPasswordField passwordField = new JPasswordField();
                        JCheckBox createDeleteDBCheckBox = new JCheckBox("Создание/удаление базы данных");
                        JCheckBox allowLoginCheckBox = new JCheckBox("Разрешен вход");
                        JCheckBox superuserCheckBox = new JCheckBox("Superuser");
                        JCheckBox createRolesCheckBox = new JCheckBox("Создание ролей");
                        JCheckBox inheritCheckBox = new JCheckBox("Наследует права от родительских ролей");
                        JCheckBox replicationCheckBox = new JCheckBox("Может создавать потоковую репликацию и резервные копии");
                        JCheckBox bypassRLSCheckBox = new JCheckBox("Bypass RLS");

                        createDeleteDBCheckBox.setSelected(rolePrivileges.contains("Создание/удаление базы данных: есть"));
                        allowLoginCheckBox.setSelected(rolePrivileges.contains("Разрешен вход: есть"));
                        superuserCheckBox.setSelected(rolePrivileges.contains("Superuser: есть"));
                        createRolesCheckBox.setSelected(rolePrivileges.contains("Создание ролей: есть"));
                        inheritCheckBox.setSelected(rolePrivileges.contains("Наследует права от родительских ролей: есть"));
                        replicationCheckBox.setSelected(rolePrivileges.contains("Может создавать потоковую репликацию и резервные копии: есть"));
                        bypassRLSCheckBox.setSelected(rolePrivileges.contains("Bypass RLS: есть"));

                        inputPanel.add(new JLabel("Логин:"));
                        inputPanel.add(usernameField);
                        inputPanel.add(new JLabel("Пароль:"));
                        inputPanel.add(passwordField);
                        inputPanel.add(new JLabel("Права доступа:"));
                        inputPanel.add(createDeleteDBCheckBox);
                        inputPanel.add(allowLoginCheckBox);
                        inputPanel.add(superuserCheckBox);
                        inputPanel.add(createRolesCheckBox);
                        inputPanel.add(inheritCheckBox);
                        inputPanel.add(replicationCheckBox);
                        inputPanel.add(bypassRLSCheckBox);

                        int confirmResult = JOptionPane.showConfirmDialog(rolesFrame, inputPanel,
                                "Введите новые данные для роли " + selectedRole, JOptionPane.OK_CANCEL_OPTION);

                        if (confirmResult == JOptionPane.OK_OPTION) {
                            String username = usernameField.getText();
                            String password = new String(passwordField.getPassword());
                            boolean createDeleteDB = createDeleteDBCheckBox.isSelected();
                            boolean allowLogin = allowLoginCheckBox.isSelected();
                            boolean superuser = superuserCheckBox.isSelected();
                            boolean createRoles = createRolesCheckBox.isSelected();
                            boolean inherit = inheritCheckBox.isSelected();
                            boolean replication = replicationCheckBox.isSelected();
                            boolean bypassRLS = bypassRLSCheckBox.isSelected();

                            rolesManager.updateRole(selectedRole, username, password, createDeleteDB, allowLogin, superuser, createRoles, inherit, replication, bypassRLS);

                            JOptionPane.showMessageDialog(rolesFrame, "Права для роли \"" + selectedRole + "\" успешно обновлены");
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(rolesFrame, "Ошибка при изменении прав роли: " + ex.getMessage());
                }
            }
        });

        panel.add(viewRolesButton);
        panel.add(addRoleButton);
        panel.add(deleteRolesButton);
        panel.add(viewPermissionsButton);
        panel.add(changePermissionsButton);

        rolesFrame.add(panel, BorderLayout.CENTER);

        rolesFrame.setVisible(true);
    }
}
