import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;
import java.util.ArrayList;

public class GUI {
    private JFrame frame;
    private DatabaseManager dbManager;
    private Connection connection;
    private String username;
    private String password;
    private String dbPrem;

    public GUI(DatabaseManager dbManager, Connection connection, String username, String password, String dbPrem) {
        this.dbManager = dbManager;
        this.connection = connection;
        this.username = username;
        this.password = password;
        this.dbPrem = dbPrem;
    }

    public void createAndShowGUI() {
        frame = new JFrame("Система управления базами данных");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(500, 800);
        frame.setLayout(new BorderLayout());
        frame.setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(17, 1, 5, 5));

        // Кнопка для создания новой базы данных
        JButton createDBButton = new JButton("Создать базу данных");
        createDBButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String dbName = JOptionPane.showInputDialog(frame, "Введите название новой базы данных:");
                if (dbName != null && !dbName.isEmpty()) {
                    try {
                        dbManager.createDatabase(dbName);
                        JOptionPane.showMessageDialog(frame, "База данных \"" + dbName + "\" успешно создана!");
                    } catch (SQLException ex) {
                        JOptionPane.showMessageDialog(frame, ex.getMessage());
                    }
                }
            }
        });

        // Кнопка для удаления базы данных
        JButton deleteDBButton = new JButton("Удалить базу данных");
        deleteDBButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных для удаления.");
                        return;
                    }

                    JPanel databasesPanel = new JPanel();
                    databasesPanel.setLayout(new GridLayout(databases.size(), 1));
                    ArrayList<JCheckBox> dbCheckBoxes = new ArrayList<>();

                    for (String db : databases) {
                        JCheckBox checkBox = new JCheckBox(db);
                        dbCheckBoxes.add(checkBox);
                        databasesPanel.add(checkBox);
                    }

                    int result = JOptionPane.showConfirmDialog(frame, databasesPanel,
                            "Выберите базы данных для удаления", JOptionPane.OK_CANCEL_OPTION);

                    if (result == JOptionPane.OK_OPTION) {
                        for (JCheckBox checkBox : dbCheckBoxes) {
                            if (checkBox.isSelected()) {
                                String selectedDB = checkBox.getText();
                                int confirm = JOptionPane.showConfirmDialog(frame, "Вы уверены, что хотите удалить базу данных \"" + selectedDB + "\"?",
                                        "Подтверждение удаления", JOptionPane.YES_NO_OPTION);
                                if (confirm == JOptionPane.YES_OPTION) {
                                    try {
                                        dbManager.dropDatabase(selectedDB);
                                        JOptionPane.showMessageDialog(frame, "База данных \"" + selectedDB + "\" успешно удалена!");
                                    } catch (SQLException ex) {
                                        JOptionPane.showMessageDialog(frame, ex.getMessage());
                                    }
                                }
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для создания таблицы
        JButton createTableButton = new JButton("Создать таблицу");
        createTableButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных для создания таблицы.");
                        return;
                    }

                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Создание таблицы", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));

                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        String tableName = JOptionPane.showInputDialog(frame, "Введите имя таблицы:");
                        if (tableName != null && !tableName.isEmpty()) {
                            try {
                                dbPrem = selectedDB;
                                dbManager.createTable(dbPrem, tableName);

                                JOptionPane.showMessageDialog(frame, "Таблица \"" + tableName + "\" успешно создана в базе данных \"" + dbPrem + "\"!");
                            } catch (SQLException ex) {
                                JOptionPane.showMessageDialog(frame, ex.getMessage());
                            }
                        } else {
                            JOptionPane.showMessageDialog(frame, "Имя таблицы не может быть пустым.");
                        }

                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для добавления столбцов в таблицу
        JButton addColumnsButton = new JButton("Добавить столбец в таблицу");
        addColumnsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Добавление столбца в таблицу", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Добавление столбца в таблицу", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            String columnName = JOptionPane.showInputDialog(frame,
                                    "Введите название столбца:", "Название столбца...");
                            if (columnName != null && !columnName.isEmpty()) {
                                dbManager.addColumn(selectedDB, selectedTable, columnName);
                                JOptionPane.showMessageDialog(frame, "Столбец \"" + columnName + "\" успешно добавлен в таблицу \"" + selectedTable + "\".");
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для удаления таблицы
        JButton deleteTableButton = new JButton("Удалить таблицу");
        deleteTableButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Удаление таблицы", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }

                        JPanel tablesPanel = new JPanel();
                        tablesPanel.setLayout(new GridLayout(tables.size(), 1));
                        ArrayList<JCheckBox> tableCheckBoxes = new ArrayList<>();

                        for (String table : tables) {
                            JCheckBox checkBox = new JCheckBox(table);
                            tableCheckBoxes.add(checkBox);
                            tablesPanel.add(checkBox);
                        }

                        int result = JOptionPane.showConfirmDialog(frame, tablesPanel,
                                "Выберите таблицы для удаления", JOptionPane.OK_CANCEL_OPTION);

                        if (result == JOptionPane.OK_OPTION) {
                            for (JCheckBox checkBox : tableCheckBoxes) {
                                if (checkBox.isSelected()) {
                                    String selectedTable = checkBox.getText();
                                    int confirm = JOptionPane.showConfirmDialog(frame, "Вы уверены, что хотите удалить таблицу \"" + selectedTable + "\" из базы данных \"" + selectedDB + "\"?",
                                            "Подтверждение удаления", JOptionPane.YES_NO_OPTION);
                                    if (confirm == JOptionPane.YES_OPTION) {
                                        try {
                                            dbManager.dropTable(selectedDB, selectedTable);
                                            JOptionPane.showMessageDialog(frame, "Таблица \"" + selectedTable + "\" успешно удалена из базы данных \"" + selectedDB + "\"!");
                                        } catch (SQLException ex) {
                                            JOptionPane.showMessageDialog(frame, ex.getMessage());
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для удаления столбца из таблицы
        JButton deleteColumnButton = new JButton("Удалить столбец из таблицы");
        deleteColumnButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Удаление столбца из таблицы", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Удаление столбца из таблицы", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            ArrayList<String> allColumns = dbManager.getAllColumns(selectedDB, selectedTable);
                            if (allColumns.isEmpty()) {
                                JOptionPane.showMessageDialog(frame, "В таблице \"" + selectedTable + "\" нет столбцов.");
                                return;
                            }

                            JPanel columnsPanel = new JPanel();
                            columnsPanel.setLayout(new GridLayout(allColumns.size(), 1));
                            ArrayList<JCheckBox> columnCheckBoxes = new ArrayList<>();

                            for (String column : allColumns) {
                                JCheckBox checkBox = new JCheckBox(column);
                                columnCheckBoxes.add(checkBox);
                                columnsPanel.add(checkBox);
                            }

                            int result = JOptionPane.showConfirmDialog(frame, columnsPanel,
                                    "Выберите столбцы для удаления", JOptionPane.OK_CANCEL_OPTION);

                            if (result == JOptionPane.OK_OPTION) {
                                for (JCheckBox checkBox : columnCheckBoxes) {
                                    if (checkBox.isSelected()) {
                                        String selectedColumn = checkBox.getText();
                                        try {
                                            dbManager.dropColumn(selectedDB, selectedTable, selectedColumn);
                                            JOptionPane.showMessageDialog(frame, "Столбец \"" + selectedColumn + "\" успешно удален!");
                                        } catch (SQLException ex) {
                                            JOptionPane.showMessageDialog(frame, ex.getMessage());
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для добавления новых данных
        JButton addDataButton = new JButton("Добавить новые данные");
        addDataButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Добавление новых данных", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Добавление новых данных", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            ArrayList<String> columnTypes = dbManager.getColumnTypes(selectedDB, selectedTable);
                            int columnCount = dbManager.getColumnCount(selectedDB, selectedTable);
                            JTextField[] dataFields = new JTextField[columnCount];
                            JPanel panel = new JPanel(new GridLayout(columnCount, 2));
                            for (int i = 0; i < columnCount; i++) {
                                JLabel label = new JLabel((i + 1) + ". " + columnTypes.get(i) + ":");
                                dataFields[i] = new JTextField(10);
                                if (columnTypes.get(i).equals("INT")) {
                                    dataFields[i].setDocument(new IntegerDocument());
                                }
                                panel.add(label);
                                panel.add(dataFields[i]);
                            }
                            int result = JOptionPane.showConfirmDialog(frame, panel, "Добавление новых данных",
                                    JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
                            if (result == JOptionPane.OK_OPTION) {
                                Object[] rowData = new Object[columnCount];
                                for (int i = 0; i < columnCount; i++) {
                                    rowData[i] = dataFields[i].getText();
                                }
                                dbManager.insertData(selectedDB, selectedTable, rowData);
                                JOptionPane.showMessageDialog(frame, "Новые данные успешно добавлены в таблицу \"" + selectedTable + "\".");
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для очистки таблицы
        JButton clearTableButton = new JButton("Очистить таблицу");
        clearTableButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Очистка таблицы", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Очистка таблицы", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            int result = JOptionPane.showConfirmDialog(frame, "Вы уверены, что хотите очистить таблицу \"" + selectedTable + "\"?", "Подтверждение очистки таблицы", JOptionPane.YES_NO_OPTION);
                            if (result == JOptionPane.YES_OPTION) {
                                dbManager.clearTable(selectedDB, selectedTable);
                                JOptionPane.showMessageDialog(frame, "Таблица \"" + selectedTable + "\" успешно очищена.");
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для просмотра содержимого таблицы
        JButton viewTableButton = new JButton("Просмотреть таблицу");
        viewTableButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Просмотр таблицы", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Просмотр таблицы", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            String tableContent = dbManager.getTableContent(selectedDB, selectedTable);
                            JOptionPane.showMessageDialog(frame, "Содержимое таблицы \"" + selectedTable + "\":\n\n" + tableContent);
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для редактирования записи в таблице
        JButton editRowButton = new JButton("Редактировать запись в таблице");
        editRowButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Редактирование записи в таблице", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Редактирование записи в таблице", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            ArrayList<String> rows = dbManager.getTableRows(selectedDB, selectedTable);
                            if (rows.isEmpty()) {
                                JOptionPane.showMessageDialog(frame, "В таблице \"" + selectedTable + "\" нет записей.");
                                return;
                            }
                            String selectedRow = (String) JOptionPane.showInputDialog(frame, "Выберите запись:",
                                    "Редактирование записи в таблице", JOptionPane.QUESTION_MESSAGE, null,
                                    rows.toArray(), rows.get(0));
                            if (selectedRow != null && !selectedRow.isEmpty()) {
                                ArrayList<String> columns = dbManager.getTableColumns(selectedDB, selectedTable);
                                if (columns.isEmpty()) {
                                    JOptionPane.showMessageDialog(frame, "В таблице \"" + selectedTable + "\" нет столбцов.");
                                    return;
                                }
                                String selectedColumn = (String) JOptionPane.showInputDialog(frame, "Выберите столбец для редактирования:",
                                        "Редактирование записи в таблице", JOptionPane.QUESTION_MESSAGE, null,
                                        columns.toArray(), columns.get(0));
                                if (selectedColumn != null && !selectedColumn.isEmpty()) {
                                    int rowIndex = rows.indexOf(selectedRow) + 1;
                                    String previousValue = dbManager.getPreviousColumnValue(selectedDB, selectedTable, rowIndex, selectedColumn);
                                    String newValue = JOptionPane.showInputDialog(frame, "Введите новое значение для столбца \"" + selectedColumn + "\":", previousValue);


                                    if (newValue != null) {
                                        dbManager.updateTableRow(selectedDB, selectedTable, rowIndex, selectedColumn, newValue);
                                        JOptionPane.showMessageDialog(frame, "Запись успешно отредактирована.");
                                    }
                                }


                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для переименования базы данных
        JButton renameDBButton = new JButton("Переименовать базу данных");
        renameDBButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных для переименования:",
                            "Переименование базы данных", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        boolean isDBInUse = dbManager.isDatabaseInUse(selectedDB);
                        if (isDBInUse) {
                            JOptionPane.showMessageDialog(frame, "База данных \"" + selectedDB + "\" занята другими пользователями.");
                            return;
                        }
                        String newDBName = JOptionPane.showInputDialog(frame, "Введите новое имя для базы данных \"" + selectedDB + "\":");
                        if (newDBName != null && !newDBName.isEmpty()) {
                            dbManager.renameDatabase(selectedDB, newDBName);
                            JOptionPane.showMessageDialog(frame, "База данных успешно переименована в \"" + newDBName + "\".");
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для переименования таблицы
        JButton renameTableButton = new JButton("Переименовать таблицу");
        renameTableButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Переименование таблицы", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу для переименования:",
                                "Переименование таблицы", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            String newTableName = JOptionPane.showInputDialog(frame, "Введите новое имя для таблицы \"" + selectedTable + "\":");
                            if (newTableName != null && !newTableName.isEmpty()) {
                                dbManager.renameTable(selectedDB, selectedTable, newTableName);
                                JOptionPane.showMessageDialog(frame, "Таблица успешно переименована.");
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для поиска по значению
        JButton searchButton = new JButton("Поиск");
        searchButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Поиск в таблице", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Поиск в таблице", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            ArrayList<String> columns = dbManager.getTableColumns(selectedDB, selectedTable);
                            if (columns.isEmpty()) {
                                JOptionPane.showMessageDialog(frame, "В таблице \"" + selectedTable + "\" нет столбцов.");
                                return;
                            }
                            String selectedColumn = (String) JOptionPane.showInputDialog(frame, "Выберите столбец для поиска:",
                                    "Поиск в таблице", JOptionPane.QUESTION_MESSAGE, null,
                                    columns.toArray(), columns.get(0));
                            if (selectedColumn != null && !selectedColumn.isEmpty()) {
                                String searchValue = JOptionPane.showInputDialog(frame, "Введите значение для поиска:");
                                if (searchValue != null && !searchValue.isEmpty()) {
                                    String searchResult = dbManager.searchInTable(selectedDB, selectedTable, selectedColumn, searchValue);
                                    JOptionPane.showMessageDialog(frame, searchResult);
                                }
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка для удалению по значению
        JButton deleteByValueButton = new JButton("Удалить по значению");
        deleteByValueButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Удаление по значению", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        ArrayList<String> tables = dbManager.getAllTables(selectedDB);
                        if (tables.isEmpty()) {
                            JOptionPane.showMessageDialog(frame, "В базе данных \"" + selectedDB + "\" нет таблиц.");
                            return;
                        }
                        String selectedTable = (String) JOptionPane.showInputDialog(frame, "Выберите таблицу:",
                                "Удаление по значению", JOptionPane.QUESTION_MESSAGE, null,
                                tables.toArray(), tables.get(0));
                        if (selectedTable != null && !selectedTable.isEmpty()) {
                            ArrayList<String> columns = dbManager.getTableColumns(selectedDB, selectedTable);
                            if (columns.isEmpty()) {
                                JOptionPane.showMessageDialog(frame, "В таблице \"" + selectedTable + "\" нет столбцов.");
                                return;
                            }
                            String selectedColumn = (String) JOptionPane.showInputDialog(frame, "Выберите столбец для удаления по значению:",
                                    "Удаление по значению", JOptionPane.QUESTION_MESSAGE, null,
                                    columns.toArray(), columns.get(0));
                            if (selectedColumn != null && !selectedColumn.isEmpty()) {
                                String valueToDelete = JOptionPane.showInputDialog(frame, "Введите значение для удаления:");
                                if (valueToDelete != null && !valueToDelete.isEmpty()) {
                                    int rowsDeleted = dbManager.deleteRowsByValue(selectedDB, selectedTable, selectedColumn, valueToDelete);
                                    JOptionPane.showMessageDialog(frame, "Удалено " + rowsDeleted + " строк с указанным значением.");
                                }
                            }
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка очистки базы данных
        JButton clearDatabaseButton = new JButton("Очистить базу данных");
        clearDatabaseButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    ArrayList<String> databases = dbManager.getAllDatabases();
                    if (databases.isEmpty()) {
                        JOptionPane.showMessageDialog(frame, "Нет доступных баз данных.");
                        return;
                    }
                    String selectedDB = (String) JOptionPane.showInputDialog(frame, "Выберите базу данных:",
                            "Очистка базы данных", JOptionPane.QUESTION_MESSAGE, null,
                            databases.toArray(), databases.get(0));
                    if (selectedDB != null && !selectedDB.isEmpty()) {
                        int option = JOptionPane.showConfirmDialog(frame, "Вы уверены, что хотите очистить все таблицы в базе данных \"" + selectedDB + "\"?", "Подтверждение очистки", JOptionPane.YES_NO_OPTION);
                        if (option == JOptionPane.YES_OPTION) {
                            // Выполняем очистку всех таблиц в выбранной базе данных
                            dbManager.clearAllTables(selectedDB);
                            JOptionPane.showMessageDialog(frame, "Все таблицы в базе данных \"" + selectedDB + "\" были очищены.");
                        }
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, ex.getMessage());
                }
            }
        });

        // Кнопка "Роли"
        JButton rolesButton = new JButton("Роли");
        rolesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                RolesWindow rolesWindow = new RolesWindow(connection);
                rolesWindow.createAndShowRolesWindow();
            }
        });

        // Кнопка для выхода
        JButton exitButton = new JButton("Выход");
        exitButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                frame.dispose();
                MainClass mainClass = new MainClass();
                mainClass.showLogin();
            }
        });

        panel.add(createDBButton); // Кнопка создать бд
        panel.add(deleteDBButton); // Кнопка удалить бд
        panel.add(createTableButton); // Кнопка создать таблицу
        panel.add(deleteTableButton); // Кнопка удалить таблицу
        panel.add(addColumnsButton); // Кнопка добавить столбец
        panel.add(deleteColumnButton); // Кнопка удалить столбец
        panel.add(addDataButton); // Кнопка добавить данные
        panel.add(clearTableButton); // Кнопка очистить таблицу
        panel.add(clearDatabaseButton); // Кнопка очистить бд
        panel.add(viewTableButton); // Кнопка просмостра таблицы
        panel.add(editRowButton); // Кнопка редактирования данных
        panel.add(renameDBButton); // Кнопка переименовывания бд
        panel.add(renameTableButton); // Кнопка переименовывания таблицы
        panel.add(searchButton); // Кнопка поиска
        panel.add(deleteByValueButton); // Кнопка удаления значения
        panel.add(rolesButton); // Кнопка ролей
        panel.add(exitButton); // Кнопка выхода

        frame.add(panel, BorderLayout.CENTER);

        frame.setVisible(true);
    }
}
