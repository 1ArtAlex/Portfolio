import java.sql.*;
import java.util.ArrayList;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;


public class DatabaseManager {
    private Connection connection;

    public DatabaseManager(Connection connection) {
        this.connection = connection;
    }

    // Метод для создания базы данных
    public void createDatabase(String databaseName) throws SQLException {
        String sql = "CREATE DATABASE " + databaseName;
        try (Statement statement = connection.createStatement()) {
            statement.executeUpdate(sql);
        }
    }

    // Метод для удаления базы данных
    public void dropDatabase(String databaseName) throws SQLException {
        String sql = "DROP DATABASE IF EXISTS " + databaseName;
        try (Statement statement = connection.createStatement()) {
            statement.executeUpdate(sql);
        }
    }

    // Метод для получения списка всех баз данных по алфавиту
    public ArrayList<String> getAllDatabases() throws SQLException {
        ArrayList<String> databases = new ArrayList<>();
        String sql = "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname";
        try (Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery(sql)) {
            while (resultSet.next()) {
                String dbName = resultSet.getString("datname");
                databases.add(dbName);
            }
        }
        return databases;
    }

    // Метод для создания таблицы
    public void createTable(String dbPrem, String tableName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbPrem;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "CREATE TABLE " + tableName + " ()";
            try (Statement statement = connection.createStatement()) {
                statement.executeUpdate(sql);
            }
        }
    }

    // Метод для получения списка всех таблиц по алфавиту
    public ArrayList<String> getAllTables(String dbPrem) throws SQLException {
        ArrayList<String> tables = new ArrayList<>();
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbPrem;
        String username = "postgres";
        String password = "I4seeyiseey";

        String sql = "SELECT table_name FROM information_schema.tables WHERE table_catalog = ? AND table_schema = 'public' ORDER BY table_name ASC";

        try (Connection connection = DriverManager.getConnection(url, username, password);
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, dbPrem);
            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    String tableName = resultSet.getString("table_name");
                    tables.add(tableName);
                }
            }
        }
        return tables;
    }

    // Метод для добавления столбца в указанную таблицу в указанной базе данных с текстовым форматом данных по умолчанию
    public void addColumn(String dbName, String tableName, String columnName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "ALTER TABLE " + tableName + " ADD COLUMN " + columnName + " TEXT";
            try (Statement statement = connection.createStatement()) {
                statement.executeUpdate(sql);
            }
        }
    }

    // Метод для удаления таблицы
    public void dropTable(String dbName, String tableName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password);
             Statement stmt = connection.createStatement()) {
            String sql = "DROP TABLE " + tableName;
            stmt.executeUpdate(sql);
        }
    }

    // Метод для получения списка всех столбцов из таблицы
    public ArrayList<String> getAllColumns(String dbName, String tableName) throws SQLException {
        ArrayList<String> columns = new ArrayList<>();
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password);
             Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery("SELECT * FROM " + tableName + " LIMIT 0")) {

            ResultSetMetaData metaData = resultSet.getMetaData();
            int columnCount = metaData.getColumnCount();
            for (int i = 1; i <= columnCount; i++) {
                String columnName = metaData.getColumnName(i);
                columns.add(columnName);
            }
        }

        return columns;
    }

    // Метод для удаления столбца из таблицы
    public void dropColumn(String dbName, String tableName, String columnName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        Connection connection = DriverManager.getConnection(url, username, password);
        Statement stmt = null;
        try {
            stmt = connection.createStatement();
            String sql = "ALTER TABLE " + tableName + " DROP COLUMN " + columnName;
            stmt.executeUpdate(sql);
        } finally {
            if (stmt != null) {
                stmt.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }

    // Метод для получения списка типов данных столбцов таблицы
    public ArrayList<String> getColumnTypes(String dbName, String tableName) throws SQLException {
        ArrayList<String> columnTypes = new ArrayList<>();
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password);
             Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery("SELECT * FROM " + tableName + " LIMIT 1")) {
            ResultSetMetaData metaData = resultSet.getMetaData();
            int columnCount = metaData.getColumnCount();
            for (int i = 1; i <= columnCount; i++) {
                String columnType = metaData.getColumnTypeName(i);
                columnTypes.add(columnType);
            }
        }
        return columnTypes;
    }

    // Метод для получения количества столбцов в таблице
    public int getColumnCount(String dbName, String tableName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password);
             Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery("SELECT * FROM " + tableName + " LIMIT 1")) {
            ResultSetMetaData metaData = resultSet.getMetaData();
            return metaData.getColumnCount();
        }
    }

    // Метод для вставки новых данных в указанную таблицу в указанной базе данных
    public void insertData(String dbName, String tableName, Object[] data) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            StringBuilder sql = new StringBuilder("INSERT INTO " + tableName + " VALUES (");
            for (int i = 0; i < data.length; i++) {
                if (data[i] instanceof String) {
                    sql.append("?,");
                } else if (data[i] instanceof Integer) {
                    sql.append("CAST(? AS INTEGER),");
                }
            }
            sql.deleteCharAt(sql.length() - 1);
            sql.append(")");

            try (PreparedStatement statement = connection.prepareStatement(sql.toString())) {
                int parameterIndex = 1;
                for (int i = 0; i < data.length; i++) {
                    if (data[i] instanceof String) {
                        statement.setString(parameterIndex++, (String) data[i]);
                    } else if (data[i] instanceof Integer) {
                        statement.setInt(parameterIndex++, (Integer) data[i]);
                    }
                }
                statement.executeUpdate();
            }
        }
    }

    // Метод для очистки таблицы
    public void clearTable(String dbName, String tableName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "DELETE FROM " + tableName;
            try (Statement statement = connection.createStatement()) {
                statement.executeUpdate(sql);
            }
        }
    }

    // Метод для получения содержимого таблицы в формате HTML
    public String getTableContent(String dbName, String tableName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        StringBuilder tableContent = new StringBuilder();
        tableContent.append("<html><body><table border=\"1\">");
        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "SELECT * FROM " + tableName;
            try (Statement statement = connection.createStatement();
                 ResultSet resultSet = statement.executeQuery(sql)) {
                ResultSetMetaData metaData = resultSet.getMetaData();
                int columnCount = metaData.getColumnCount();
                tableContent.append("<tr>");
                for (int i = 1; i <= columnCount; i++) {
                    tableContent.append("<th>").append(metaData.getColumnName(i)).append("</th>");
                }
                tableContent.append("</tr>");
                while (resultSet.next()) {
                    tableContent.append("<tr>");
                    for (int i = 1; i <= columnCount; i++) {
                        tableContent.append("<td>").append(resultSet.getString(i)).append("</td>");
                    }
                    tableContent.append("</tr>");
                }
            }
        }
        tableContent.append("</table></body></html>");
        return tableContent.toString();
    }

    // Метод для обновления значения в указанной записи и столбце таблицы
    public void updateTableRow(String dbName, String tableName, int rowIndex, String columnName, String newValue) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "UPDATE " + tableName + " SET " + columnName + " = ? WHERE ctid = (SELECT ctid FROM " + tableName + " OFFSET ? LIMIT 1)";
            try (PreparedStatement statement = connection.prepareStatement(sql)) {
                statement.setString(1, newValue);
                statement.setInt(2, rowIndex - 1);
                statement.executeUpdate();
            }
        }
    }

    // Метод для получения списка столбцов таблицы
    public ArrayList<String> getTableColumns(String dbName, String tableName) throws SQLException {
        ArrayList<String> columns = new ArrayList<>();
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            DatabaseMetaData metaData = connection.getMetaData();
            try (ResultSet resultSet = metaData.getColumns(null, null, tableName, null)) {
                while (resultSet.next()) {
                    String columnName = resultSet.getString("COLUMN_NAME");
                    columns.add(columnName);
                }
            }
        }
        return columns;
    }

    // Метод для получения списка строк (записей) таблицы
    public ArrayList<String> getTableRows(String dbName, String tableName) throws SQLException {
        ArrayList<String> rows = new ArrayList<>();
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "SELECT * FROM " + tableName;
            try (Statement statement = connection.createStatement();
                 ResultSet resultSet = statement.executeQuery(sql)) {
                ResultSetMetaData metaData = resultSet.getMetaData();
                while (resultSet.next()) {
                    StringBuilder row = new StringBuilder();
                    for (int i = 1; i <= metaData.getColumnCount(); i++) {
                        row.append(resultSet.getString(i)).append(" ");
                    }
                    rows.add(row.toString().trim());
                }
            }
        }
        return rows;
    }

    // Метод для получения предыдущего значения столбца для выбранной записи
    public String getPreviousColumnValue(String dbName, String tableName, int rowIndex, String selectedColumn) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";
        String previousValue = null;

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "SELECT " + selectedColumn + " FROM " + tableName + " OFFSET ? LIMIT 1";
            try (PreparedStatement statement = connection.prepareStatement(sql)) {
                statement.setInt(1, rowIndex - 1);
                try (ResultSet resultSet = statement.executeQuery()) {
                    if (resultSet.next()) {
                        previousValue = resultSet.getString(selectedColumn);
                    }
                }
            }
        }
        return previousValue;
    }

    // Метод для переименования базы данных
    public void renameDatabase(String oldName, String newName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "ALTER DATABASE " + oldName + " RENAME TO " + newName;
            try (Statement statement = connection.createStatement()) {
                statement.executeUpdate(sql);
            }
        }
    }

    // Метод для проверки, используется ли база данных другими пользователями
    public boolean isDatabaseInUse(String dbName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "SELECT count(*) FROM pg_stat_activity WHERE datname = ?";
            try (PreparedStatement statement = connection.prepareStatement(sql)) {
                statement.setString(1, dbName);
                try (ResultSet resultSet = statement.executeQuery()) {
                    if (resultSet.next()) {
                        int activeSessionsCount = resultSet.getInt(1);
                        return activeSessionsCount > 0;
                    }
                }
            }
        }
        return true;
    }

    // Метод для переименования таблицы
    public void renameTable(String dbName, String oldTableName, String newTableName) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "ALTER TABLE " + oldTableName + " RENAME TO " + newTableName;
            try (Statement statement = connection.createStatement()) {
                statement.executeUpdate(sql);
            }
        }
    }

    // Метод для поиска в таблице
    public String searchInTable(String dbName, String tableName, String columnName, String searchValue) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        StringBuilder searchResult = new StringBuilder();
        searchResult.append("<html><body><table border=\"1\">");
        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "SELECT * FROM " + tableName + " WHERE " + columnName + " LIKE ?";
            try (PreparedStatement statement = connection.prepareStatement(sql)) {
                statement.setString(1, "%" + searchValue + "%");
                try (ResultSet resultSet = statement.executeQuery()) {
                    ResultSetMetaData metaData = resultSet.getMetaData();
                    int columnCount = metaData.getColumnCount();
                    searchResult.append("<tr>");
                    for (int i = 1; i <= columnCount; i++) {
                        searchResult.append("<th>").append(metaData.getColumnName(i)).append("</th>");
                    }
                    searchResult.append("</tr>");
                    while (resultSet.next()) {
                        searchResult.append("<tr>");
                        for (int i = 1; i <= columnCount; i++) {
                            searchResult.append("<td>").append(resultSet.getString(i)).append("</td>");
                        }
                        searchResult.append("</tr>");
                    }
                }
            }
        }
        searchResult.append("</table></body></html>");
        return searchResult.toString();
    }

    // Метод для удаления данных по значению
    public int deleteRowsByValue(String dbName, String tableName, String columnName, String valueToDelete) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/" + dbName;
        String username = "postgres";
        String password = "I4seeyiseey";

        int rowsDeleted = 0;
        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String sql = "DELETE FROM " + tableName + " WHERE " + columnName + " = ?";
            try (PreparedStatement statement = connection.prepareStatement(sql)) {
                statement.setString(1, valueToDelete);
                rowsDeleted = statement.executeUpdate();
            }
        }
        return rowsDeleted;
    }

    // Метод для очистки бд
    public void clearAllTables(String dbName) throws SQLException {
        ArrayList<String> tables = getAllTables(dbName);
        for (String table : tables) {
            dropTable(dbName, table);
        }
    }
}


