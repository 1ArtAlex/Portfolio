import javax.swing.*;
import java.sql.*;
import java.awt.BorderLayout;
import java.util.ArrayList;
import java.sql.Statement;


public class RolesManager {
    private Connection connection;
    private Statement statement;

    public RolesManager(Connection connection) {
        this.connection = connection;
        try {
            this.statement = connection.createStatement();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Метод для вывода ролей
    public void showAllRoles() {
        JFrame rolesFrame = new JFrame("Список ролей");
        rolesFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // закрыть только это окно
        rolesFrame.setSize(400, 300);
        rolesFrame.setLayout(new BorderLayout());
        rolesFrame.setLocationRelativeTo(null);

        DefaultListModel<String> listModel = new DefaultListModel<>();
        JList<String> rolesList = new JList<>(listModel);
        JScrollPane scrollPane = new JScrollPane(rolesList);
        rolesFrame.add(scrollPane, BorderLayout.CENTER);

        try {
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT rolname FROM pg_roles WHERE rolname !~ '^pg_' AND rolname <> 'postgres' ORDER BY rolname");
            while (resultSet.next()) {
                String roleName = resultSet.getString("rolname");
                listModel.addElement(roleName);
            }
            statement.close();
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(rolesFrame, "Ошибка при получении списка ролей: " + ex.getMessage());
        }

        rolesFrame.setVisible(true);
    }

    // Метод добавления ролей
    public void addRole(String username, String password, boolean createDeleteDB, boolean inherit,
                        boolean allowLogin, boolean superuser, boolean createRoles, boolean replication, boolean bypassRLS) throws SQLException {
        try (Statement statement = connection.createStatement()) {
            String createUserSql = "CREATE USER " + username + " WITH PASSWORD '" + password + "'";
            statement.executeUpdate(createUserSql);
        }

        if (createRoles) {
            try (Statement statement = connection.createStatement()) {
                ResultSet resultSet = statement.executeQuery("SELECT 1 FROM pg_roles WHERE rolname = '" + username + "'");
                if (!resultSet.next()) {
                    String createRoleSql = "CREATE ROLE " + username;
                    statement.executeUpdate(createRoleSql);
                }
            }
        }

        try (Statement statement = connection.createStatement()) {
            // Права на создание/удаление базы данных
            if (createDeleteDB) {
                statement.executeUpdate("ALTER USER " + username + " CREATEDB");
            } else {
                statement.executeUpdate("ALTER USER " + username + " NOCREATEDB");
            }
            // Права на создание/удаление ролей
            if (createRoles) {
                statement.executeUpdate("ALTER USER " + username + " CREATEROLE");
            } else {
                statement.executeUpdate("ALTER USER " + username + " NOCREATEROLE");
            }
            // Разрешение или запрет входа
            if (allowLogin) {
                statement.executeUpdate("ALTER USER " + username + " LOGIN");
            } else {
                statement.executeUpdate("ALTER USER " + username + " NOLOGIN");
            }
            // Назначение или снятие права суперпользователя
            if (superuser) {
                statement.executeUpdate("ALTER USER " + username + " SUPERUSER");
            } else {
                statement.executeUpdate("ALTER USER " + username + " NOSUPERUSER");
            }
            // Права на наследование
            if (inherit) {
                statement.executeUpdate("ALTER ROLE " + username + " INHERIT");
            } else {
                statement.executeUpdate("ALTER ROLE " + username + " NOINHERIT");
            }
            // Права на создание потоковой репликации и резервных копий
            if (replication) {
                statement.executeUpdate("ALTER ROLE " + username + " REPLICATION");
            } else {
                statement.executeUpdate("ALTER ROLE " + username + " NOREPLICATION");
            }
            // Права на Bypass RLS
            if (bypassRLS) {
                statement.executeUpdate("ALTER ROLE " + username + " BYPASSRLS");
            } else {
                statement.executeUpdate("ALTER ROLE " + username + " NOBYPASSRLS");
            }
        }
    }

    // Метод для удаления роли
    public void deleteRole(String roleName) throws SQLException {
        try (Statement statement = connection.createStatement()) {
            String dropRoleSql = "DROP ROLE IF EXISTS " + roleName;
            statement.executeUpdate(dropRoleSql);
        }
    }

    // Метод для получения списка всех ролей
    public ArrayList<String> getRoles() {
        ArrayList<String> roles = new ArrayList<>();
        try {
            try (Statement statement = connection.createStatement()) {
                String getRolesSql = "SELECT rolname FROM pg_roles WHERE rolname !~ '^pg_' AND rolname <> 'postgres' ORDER BY rolname";
                ResultSet resultSet = statement.executeQuery(getRolesSql);
                while (resultSet.next()) {
                    String roleName = resultSet.getString("rolname");
                    roles.add(roleName);
                }
            }
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
        return roles;
    }

    // Метод для вывода прав роли
    public String getRolePrivileges(String roleName) throws SQLException {
        StringBuilder privilegesBuilder = new StringBuilder();

        String sqlQuery = "SELECT rolname, " +
                "CASE WHEN rolcreatedb THEN 'есть' ELSE 'нет' END AS rolcreatedb, " +
                "CASE WHEN rolcanlogin THEN 'есть' ELSE 'нет' END AS rolcanlogin, " +
                "CASE WHEN rolsuper THEN 'есть' ELSE 'нет' END AS rolsuper, " +
                "CASE WHEN rolcreaterole THEN 'есть' ELSE 'нет' END AS rolcreaterole, " +
                "CASE WHEN rolinherit THEN 'есть' ELSE 'нет' END AS rolinherit, " +
                "CASE WHEN rolreplication THEN 'есть' ELSE 'нет' END AS rolreplication, " +
                "CASE WHEN rolbypassrls THEN 'есть' ELSE 'нет' END AS rolbypassrls " +
                "FROM pg_roles " +
                "WHERE rolname = '" + roleName + "'";

        ResultSet resultSet = statement.executeQuery(sqlQuery);

        if (resultSet.next()) {
            String createdb = resultSet.getString("rolcreatedb");
            String rolcanlogin = resultSet.getString("rolcanlogin");
            String rolsuper = resultSet.getString("rolsuper");
            String rolcreaterole = resultSet.getString("rolcreaterole");
            String rolinherit = resultSet.getString("rolinherit");
            String rolreplication = resultSet.getString("rolreplication");
            String rolbypassrls = resultSet.getString("rolbypassrls");

            privilegesBuilder.append("Создание/удаление базы данных: ").append(createdb).append("\n");
            privilegesBuilder.append("Разрешен вход: ").append(rolcanlogin).append("\n");
            privilegesBuilder.append("Superuser: ").append(rolsuper).append("\n");
            privilegesBuilder.append("Создание ролей: ").append(rolcreaterole).append("\n");
            privilegesBuilder.append("Наследует права от родительских ролей: ").append(rolinherit).append("\n");
            privilegesBuilder.append("Может создавать потоковую репликацию и резервные копии: ").append(rolreplication).append("\n");
            privilegesBuilder.append("Bypass RLS: ").append(rolbypassrls);
        }

        return privilegesBuilder.toString();
    }

    // Метод для изменение прав
    public void updateRole(String oldUsername, String newUsername, String password, boolean createDeleteDB, boolean allowLogin, boolean superuser, boolean createRoles, boolean inherit, boolean replication, boolean bypassRLS) throws SQLException {
        try (Statement outerStatement = connection.createStatement()) {
            outerStatement.executeUpdate("ALTER ROLE " + oldUsername + " RENAME TO " + newUsername);

            if (!password.isEmpty()) {
                outerStatement.executeUpdate("ALTER ROLE " + newUsername + " WITH PASSWORD '" + password + "'");
            }

            try (Statement statement = connection.createStatement()) {
                if (createDeleteDB) {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " CREATEDB");
                } else {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " NOCREATEDB");
                }

                if (allowLogin) {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " LOGIN");
                } else {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " NOLOGIN");
                }

                if (superuser) {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " SUPERUSER");
                } else {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " NOSUPERUSER");
                }

                if (createRoles) {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " CREATEROLE");
                } else {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " NOCREATEROLE");
                }

                if (inherit) {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " INHERIT");
                } else {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " NOINHERIT");
                }

                if (replication) {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " REPLICATION");
                } else {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " NOREPLICATION");
                }

                if (bypassRLS) {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " BYPASSRLS");
                } else {
                    statement.executeUpdate("ALTER ROLE " + newUsername + " NOBYPASSRLS");
                }
            }
        }
    }
}
