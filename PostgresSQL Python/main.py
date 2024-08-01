import psycopg2
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def connect_to_database():
    global root, conn
    try:
        user = username_entry.get()
        password = password_entry.get()

        conn_string = f"host=localhost port=5432 dbname=postgres user={user} password={password}"
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True

        root.withdraw()

        create_db_window = tk.Toplevel(root)
        create_db_window.title("База данных")

        create_db_window.grab_set()

        def create_database_window():
            create_database_dialog()

        def delete_database_window():
            delete_database_dialog()

        def create_table_window():
            create_table_dialog(user, password)

        def delete_table_window():
            choose_db_for_deletion(user, password)

        def add_column_window():
            choose_db_for_column(user, password)

        def delete_column_window():
            select_db_for_column_deletion(user, password)

        def view_table_window():
            choose_table_and_view(user, password)

        def add_data_window():
            add_data_to_table(user, password)

        def clear_table_window():
            clear_table_dialog(user, password)

        def edit_data_window():
            edit_data_dialog(user, password)

        def search_window():
            search_data_dialog(user, password)

        def delete_by_value_window():
            delete_data_dialog(user, password)


        def open_roles_window():
            roles_window = tk.Toplevel(create_db_window)
            roles_window.title("Роли")

            def create_role_window():
                role_window = tk.Toplevel(roles_window)
                role_window.title("Создание роли")

                def add_role():
                    role_name = role_name_entry.get()
                    role_password = role_password_entry.get()
                    create_delete_db = create_delete_db_var.get()
                    allow_login = allow_login_var.get()
                    superuser = superuser_var.get()
                    create_roles = create_roles_var.get()
                    inherit = inherit_var.get()
                    replication = replication_var.get()
                    bypass_rls = bypass_rls_var.get()

                    create_role(user, password, role_name, role_password, create_delete_db, allow_login, superuser,
                                create_roles, inherit, replication, bypass_rls)

                    role_window.destroy()

                role_name_label = tk.Label(role_window, text="Имя роли:")
                role_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
                role_name_entry = tk.Entry(role_window)
                role_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

                role_password_label = tk.Label(role_window, text="Пароль:")
                role_password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
                role_password_entry = tk.Entry(role_window, show="*")
                role_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

                create_delete_db_var = tk.BooleanVar()
                create_delete_db_checkbox = tk.Checkbutton(role_window, text="Создание/удаление базы данных",
                                                           variable=create_delete_db_var)
                create_delete_db_checkbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                allow_login_var = tk.BooleanVar()
                allow_login_checkbox = tk.Checkbutton(role_window, text="Разрешен вход", variable=allow_login_var)
                allow_login_checkbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                superuser_var = tk.BooleanVar()
                superuser_checkbox = tk.Checkbutton(role_window, text="Superuser", variable=superuser_var)
                superuser_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                create_roles_var = tk.BooleanVar()
                create_roles_checkbox = tk.Checkbutton(role_window, text="Создание ролей", variable=create_roles_var)
                create_roles_checkbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                inherit_var = tk.BooleanVar()
                inherit_checkbox = tk.Checkbutton(role_window, text="Наследует права от родительских ролей",
                                                  variable=inherit_var)
                inherit_checkbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                replication_var = tk.BooleanVar()
                replication_checkbox = tk.Checkbutton(role_window,
                                                      text="Может создавать потоковую репликацию и резервные копии",
                                                      variable=replication_var)
                replication_checkbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                bypass_rls_var = tk.BooleanVar()
                bypass_rls_checkbox = tk.Checkbutton(role_window, text="Bypass RLS", variable=bypass_rls_var)
                bypass_rls_checkbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                add_button = tk.Button(role_window, text="Добавить", command=add_role)
                add_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

            def delete_role_window():
                def delete_selected_roles():
                    selected_roles = [role for role, var in roles_vars.items() if var.get() == 1]
                    for role in selected_roles:
                        delete_role(user, password, role)
                    roles_window.destroy()

                roles_window = tk.Toplevel(create_db_window)
                roles_window.title("Удаление роли")

                roles = get_roles_list(user, password)

                roles_vars = {}
                for i, role in enumerate(roles):
                    roles_vars[role] = tk.IntVar()
                    check_button = tk.Checkbutton(roles_window, text=role, variable=roles_vars[role], onvalue=1,
                                                  offvalue=0)
                    check_button.grid(row=i, column=0, padx=5, pady=5, sticky="w")

                delete_button = tk.Button(roles_window, text="Удалить выбранные роли", command=delete_selected_roles)
                delete_button.grid(row=len(roles), column=0, padx=5, pady=10)

                roles_window.update()
                height = roles_window.winfo_height()
                roles_window.geometry(f"{300}x{height}")

            create_delete_db_var = tk.IntVar()
            allow_login_var = tk.IntVar()
            superuser_var = tk.IntVar()
            create_roles_var = tk.IntVar()
            inherit_var = tk.IntVar()
            replication_var = tk.IntVar()
            bypass_rls_var = tk.IntVar()

            def change_permissions_window():
                def apply_changes(permissions_window, role):
                    new_username = username_entry.get()  # Добавили эту строку
                    new_password = password_entry.get()
                    new_permissions = {
                        "CREATEDB": create_delete_db_var.get(),
                        "LOGIN": allow_login_var.get(),
                        "SUPERUSER": superuser_var.get(),
                        "CREATEROLE": create_roles_var.get(),
                        "INHERIT": inherit_var.get(),
                        "REPLICATION": replication_var.get(),
                        "BYPASSRLS": bypass_rls_var.get()
                    }
                    change_permissions(user, password, role, new_username, new_password, new_permissions)
                    permissions_window.destroy()

                def select_role_and_continue(roles_combobox, select_role_dialog):
                    selected_role = roles_combobox.get()
                    permissions_window = tk.Toplevel(root)
                    permissions_window.title("Изменение прав")
                    show_change_permissions_dialog(selected_role, permissions_window)
                    select_role_dialog.destroy()

                def show_change_permissions_dialog(selected_role, permissions_window):
                    global username_entry
                    global password_entry
                    clear_permissions_checkboxes()
                    set_permissions_checkboxes(selected_role)
                    permissions_window.title("Изменение прав")

                    # Поля ввода для нового логина и пароля
                    username_label = tk.Label(permissions_window, text="Новый логин:")
                    username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
                    username_entry = tk.Entry(permissions_window)
                    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

                    password_label = tk.Label(permissions_window, text="Новый пароль:")
                    password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
                    password_entry = tk.Entry(permissions_window, show="*")
                    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

                    create_delete_db_checkbox = tk.Checkbutton(permissions_window, text="Создание/удаление базы данных",
                                                               variable=create_delete_db_var)
                    create_delete_db_checkbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                    allow_login_checkbox = tk.Checkbutton(permissions_window, text="Разрешен вход",
                                                          variable=allow_login_var)
                    allow_login_checkbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                    superuser_checkbox = tk.Checkbutton(permissions_window, text="Superuser", variable=superuser_var)
                    superuser_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                    create_roles_checkbox = tk.Checkbutton(permissions_window, text="Создание ролей",
                                                           variable=create_roles_var)
                    create_roles_checkbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                    inherit_checkbox = tk.Checkbutton(permissions_window, text="Наследует права от родительских ролей",
                                                      variable=inherit_var)
                    inherit_checkbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                    replication_checkbox = tk.Checkbutton(permissions_window,
                                                          text="Может создавать потоковую репликацию и резервные копии",
                                                          variable=replication_var)
                    replication_checkbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                    bypass_rls_checkbox = tk.Checkbutton(permissions_window, text="Bypass RLS", variable=bypass_rls_var)
                    bypass_rls_checkbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="w")

                    # Кнопка для применения изменений
                    apply_button = tk.Button(permissions_window, text="Сохранить изменения",
                                             command=lambda: apply_changes(permissions_window, selected_role))

                    apply_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10)

                def clear_permissions_checkboxes():
                    create_delete_db_var.set(0)
                    allow_login_var.set(0)
                    superuser_var.set(0)
                    create_roles_var.set(0)
                    inherit_var.set(0)
                    replication_var.set(0)
                    bypass_rls_var.set(0)

                def set_permissions_checkboxes(selected_role):
                    permissions_list = get_permissions(user, password, selected_role)
                    if "CREATEDB" in permissions_list:
                        create_delete_db_var.set(1)
                    if "LOGIN" in permissions_list:
                        allow_login_var.set(1)
                    if "SUPERUSER" in permissions_list:
                        superuser_var.set(1)
                    if "CREATEROLE" in permissions_list:
                        create_roles_var.set(1)
                    if "INHERIT" in permissions_list:
                        inherit_var.set(1)
                    if "REPLICATION" in permissions_list:
                        replication_var.set(1)
                    if "BYPASSRLS" in permissions_list:
                        bypass_rls_var.set(1)

                select_role_dialog = tk.Toplevel(root)
                select_role_dialog.title("Выберите роль")
                select_role_dialog.grab_set()

                roles_label = tk.Label(select_role_dialog, text="Выберите роль:")
                roles_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

                roles_combobox = ttk.Combobox(select_role_dialog, state="readonly",
                                              values=get_roles_list(user, password))
                roles_combobox.grid(row=0, column=1, padx=5, pady=5)

                select_button = tk.Button(select_role_dialog, text="Выбрать",
                                          command=lambda: select_role_and_continue(roles_combobox, select_role_dialog))
                select_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

                select_role_dialog.mainloop()

            create_role_button = tk.Button(roles_window, text="Создать роль", command=create_role_window, width=30, height=2)
            create_role_button.grid(row=0, column=0, padx=5, pady=5)

            delete_role_button = tk.Button(roles_window, text="Удалить роль", command=delete_role_window, width=30, height=2)
            delete_role_button.grid(row=1, column=0, padx=5, pady=5)

            change_permissions_button = tk.Button(roles_window, text="Изменить или посмотреть права", command=change_permissions_window, width=30, height=2)
            change_permissions_button.grid(row=2, column=0, padx=5, pady=5)

            roles_window.update()
            height = roles_window.winfo_height()
            roles_window.geometry(f"{300}x{height}")

        create_db_button = tk.Button(create_db_window, text="Создать БД", command=create_database_window, width=20, height=2)
        create_db_button.grid(row=0, column=0, padx=5, pady=5)

        delete_db_button = tk.Button(create_db_window, text="Удалить БД", command=delete_database_window, width=20, height=2)
        delete_db_button.grid(row=1, column=0, padx=5, pady=5)

        create_table_button = tk.Button(create_db_window, text="Создать таблицу", command=create_table_window, width=20, height=2)
        create_table_button.grid(row=2, column=0, padx=5, pady=5)

        delete_table_button = tk.Button(create_db_window, text="Удалить таблицу", command=delete_table_window, width=20, height=2)
        delete_table_button.grid(row=3, column=0, padx=5, pady=5)

        add_column_button = tk.Button(create_db_window, text="Добавить столбец", command=add_column_window, width=20, height=2)
        add_column_button.grid(row=4, column=0, padx=5, pady=5)

        delete_column_button = tk.Button(create_db_window, text="Удалить столбец", command=delete_column_window, width=20, height=2)
        delete_column_button.grid(row=5, column=0, padx=5, pady=5)

        view_table_button = tk.Button(create_db_window, text="Просмотр таблицы", command=view_table_window, width=20, height=2)
        view_table_button.grid(row=6, column=0, padx=5, pady=5)

        add_data_button = tk.Button(create_db_window, text="Добавить данные", command=add_data_window, width=20, height=2)
        add_data_button.grid(row=7, column=0, padx=5, pady=5)

        clear_table_button = tk.Button(create_db_window, text="Очистить таблицу", command=clear_table_window, width=20,
                                       height=2)
        clear_table_button.grid(row=8, column=0, padx=5, pady=5)

        edit_data_button = tk.Button(create_db_window, text="Редактировать данные", command=edit_data_window, width=20,
                                     height=2)
        edit_data_button.grid(row=9, column=0, padx=5, pady=5)

        search_button = tk.Button(create_db_window, text="Поиск", command=search_window, width=20, height=2)
        search_button.grid(row=10, column=0, padx=5, pady=5)

        delete_by_value_button = tk.Button(create_db_window, text="Удалить по значению", command=delete_by_value_window,
                                           width=20, height=2)
        delete_by_value_button.grid(row=11, column=0, padx=5, pady=5)

        roles_button = tk.Button(create_db_window, text="Роли", command=open_roles_window, width=20, height=2)
        roles_button.grid(row=12, column=0, padx=5, pady=5)


        create_db_window.update_idletasks()
        height = create_db_window.winfo_height()
        create_db_window.geometry(f"{300}x{height}")

    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при подключении к базе данных: {e}")


def create_database_dialog():
    global conn

    def create_database():
        try:
            db_name = db_name_entry.get()
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {db_name};")
            messagebox.showinfo("Успех", f"База данных '{db_name}' успешно создана")
            create_db_dialog.destroy()
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании базы данных: {e}")

    create_db_dialog = tk.Toplevel(root)
    create_db_dialog.title("Создание базы данных")
    create_db_dialog.grab_set()

    db_name_label = tk.Label(create_db_dialog, text="Название базы данных:")
    db_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_name_entry = tk.Entry(create_db_dialog)
    db_name_entry.grid(row=0, column=1, padx=5, pady=5)

    create_db_button = tk.Button(create_db_dialog, text="Создать", command=create_database)
    create_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    create_db_dialog.update()
    height = create_db_dialog.winfo_height()
    create_db_dialog.geometry(f"{300}x{height}")


def delete_database_dialog():
    def delete_databases():
        try:
            for i, var in enumerate(selected_dbs):
                if var.get():
                    with conn.cursor() as cursor:
                        cursor.execute(f"DROP DATABASE {databases[i][0]};")
            messagebox.showinfo("Успех", "Выбранные базы данных успешно удалены")
            delete_db_dialog.destroy()
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении базы данных: {e}")

    delete_db_dialog = tk.Toplevel(root)
    delete_db_dialog.title("Удаление базы данных")
    delete_db_dialog.grab_set()

    with conn.cursor() as cursor:
        try:
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = cursor.fetchall()

            selected_dbs = []

            for i, db in enumerate(databases):
                var = tk.BooleanVar()
                var.set(False)
                selected_dbs.append(var)
                checkbox = ttk.Checkbutton(delete_db_dialog, text=db[0], variable=var)
                checkbox.grid(row=i, column=0, sticky="w")

            delete_db_button = tk.Button(delete_db_dialog, text="Удалить", command=delete_databases)
            delete_db_button.grid(row=len(databases), column=0, padx=5, pady=5)

            delete_db_dialog.update()
            height = delete_db_dialog.winfo_height()
            delete_db_dialog.geometry(f"{300}x{height}")

        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении списка баз данных: {e}")
            delete_db_dialog.destroy()


def create_table_dialog(user, password):
    def create_table():
        selected_db = db_combobox.get()
        table_name = table_name_entry.get()
        try:
            conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
            conn_local = psycopg2.connect(conn_string)
            with conn_local.cursor() as cursor:
                cursor.execute(f"CREATE TABLE {table_name} ();")
            conn_local.commit()
            conn_local.close()
            messagebox.showinfo("Успех", f"Таблица '{table_name}' успешно создана в базе данных '{selected_db}'")
            create_table_dialog.destroy()
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании таблицы: {e}")

    create_table_dialog = tk.Toplevel(root)
    create_table_dialog.title("Создание таблицы")
    create_table_dialog.grab_set()

    db_label = tk.Label(create_table_dialog, text="Выберите базу данных:")
    db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(create_table_dialog, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    with conn.cursor() as cursor:
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
    db_combobox['values'] = [db[0] for db in databases]

    table_name_label = tk.Label(create_table_dialog, text="Название таблицы:")
    table_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    table_name_entry = tk.Entry(create_table_dialog)
    table_name_entry.grid(row=1, column=1, padx=5, pady=5)

    create_table_button = tk.Button(create_table_dialog, text="Создать", command=create_table)
    create_table_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    create_table_dialog.update()
    height = create_table_dialog.winfo_height()
    create_table_dialog.geometry(f"{300}x{height}")


def delete_table_dialog(user, password, selected_db):
    def delete_tables():
        selected_tables = [table for table, var in zip(table_list, table_vars) if var.get()]
        try:
            conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
            conn_local = psycopg2.connect(conn_string)
            with conn_local.cursor() as cursor:
                for table in selected_tables:
                    cursor.execute(f"DROP TABLE {table};")
            conn_local.commit()
            conn_local.close()
            messagebox.showinfo("Успех", f"Выбранные таблицы успешно удалены из базы данных '{selected_db}'")
            delete_table_dialog.destroy()
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении таблиц: {e}")

    delete_table_dialog = tk.Toplevel(root)
    delete_table_dialog.title("Удаление таблиц")
    delete_table_dialog.grab_set()

    db_label = tk.Label(delete_table_dialog, text="Выбранная база данных:")
    db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    selected_db_label = tk.Label(delete_table_dialog, text=selected_db)
    selected_db_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    with psycopg2.connect(f"host=localhost port=5432 dbname={selected_db} user={user} password={password}") as conn_local:
        with conn_local.cursor() as cursor:
            cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            table_list = [table[0] for table in cursor.fetchall()]

    table_vars = [tk.BooleanVar() for _ in range(len(table_list))]
    for i, table in enumerate(table_list):
        checkbox = ttk.Checkbutton(delete_table_dialog, text=table, variable=table_vars[i])
        checkbox.grid(row=i + 1, column=0, sticky="w")

    delete_table_button = tk.Button(delete_table_dialog, text="Удалить", command=delete_tables)
    delete_table_button.grid(row=len(table_list) + 1, column=0, columnspan=2, padx=5, pady=5)

    delete_table_dialog.update()
    height = delete_table_dialog.winfo_height()
    delete_table_dialog.geometry(f"{300}x{height}")


def choose_db_for_deletion(user, password):
    def select_db_and_continue():
        selected_db = db_combobox.get()
        delete_table_dialog(user, password, selected_db)

    db_select_dialog = tk.Toplevel(root)
    db_select_dialog.title("Выбор базы данных")
    db_select_dialog.grab_set()

    db_label = tk.Label(db_select_dialog, text="Выберите базу данных:")
    db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(db_select_dialog, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    with conn.cursor() as cursor:
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
    db_combobox['values'] = [db[0] for db in databases]

    select_db_button = tk.Button(db_select_dialog, text="Выбрать", command=select_db_and_continue)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    db_select_dialog.update()
    height = db_select_dialog.winfo_height()
    db_select_dialog.geometry(f"{300}x{height}")


def choose_db_for_column(user, password):
    def select_db_and_continue(selected_db):
        choose_table_for_column(user, password, selected_db)
        db_select_dialog.destroy()

    db_select_dialog = tk.Toplevel(root)
    db_select_dialog.title("Выбор базы данных")
    db_select_dialog.grab_set()

    db_label = tk.Label(db_select_dialog, text="Выберите базу данных:")
    db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(db_select_dialog, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    with conn.cursor() as cursor:
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
    db_combobox['values'] = [db[0] for db in databases]

    select_db_button = tk.Button(db_select_dialog, text="Выбрать", command=lambda: select_db_and_continue(db_combobox.get()))
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    db_select_dialog.update()
    height = db_select_dialog.winfo_height()
    db_select_dialog.geometry(f"{300}x{height}")


def choose_table_for_column(user, password, selected_db):
    def select_table_and_continue(selected_table):
        add_column_dialog(user, password, selected_db, selected_table)
        table_select_dialog.destroy()

    table_select_dialog = tk.Toplevel(root)
    table_select_dialog.title("Выбор таблицы")
    table_select_dialog.grab_set()

    table_label = tk.Label(table_select_dialog, text="Выберите таблицу:")
    table_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    table_combobox = ttk.Combobox(table_select_dialog, state="readonly")
    table_combobox.grid(row=0, column=1, padx=5, pady=5)

    with psycopg2.connect(f"host=localhost port=5432 dbname={selected_db} user={user} password={password}") as conn_local:
        with conn_local.cursor() as cursor:
            cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = cursor.fetchall()
    table_combobox['values'] = [table[0] for table in tables]

    select_table_button = tk.Button(table_select_dialog, text="Выбрать", command=lambda: select_table_and_continue(table_combobox.get()))
    select_table_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    table_select_dialog.update()
    height = table_select_dialog.winfo_height()
    table_select_dialog.geometry(f"{300}x{height}")


def add_column_dialog(user, password, selected_db, selected_table):
    def add_column():
        column_name = column_name_entry.get()
        column_type = "TEXT"
        try:
            conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
            conn_local = psycopg2.connect(conn_string)
            with conn_local.cursor() as cursor:
                cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN {column_name} {column_type};")
            conn_local.commit()
            conn_local.close()
            messagebox.showinfo("Успех", f"Столбец '{column_name}' успешно добавлен в таблицу '{selected_table}'")
            add_column_window.destroy()
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении столбца: {e}")

    add_column_window = tk.Toplevel(root)
    add_column_window.title("Добавить столбец")
    add_column_window.grab_set()

    column_name_label = tk.Label(add_column_window, text="Название столбца:")
    column_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    column_name_entry = tk.Entry(add_column_window)
    column_name_entry.grid(row=0, column=1, padx=5, pady=5)

    add_column_button = tk.Button(add_column_window, text="Добавить", command=add_column)
    add_column_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    add_column_window.update()
    height = add_column_window.winfo_height()
    add_column_window.geometry(f"{300}x{height}")


def select_db_for_column_deletion(user, password):
    def select_table_and_continue():
        selected_db = db_combobox.get()
        if selected_db:
            choose_table_for_deletion(user, password, selected_db)
        else:
            messagebox.showerror("Ошибка", "Выберите базу данных")

    db_select_dialog = tk.Toplevel(root)
    db_select_dialog.title("Выбор базы данных")
    db_select_dialog.grab_set()

    db_label = tk.Label(db_select_dialog, text="Выберите базу данных:")
    db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(db_select_dialog, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    with conn.cursor() as cursor:
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
    db_combobox['values'] = [db[0] for db in databases]

    select_db_button = tk.Button(db_select_dialog, text="Выбрать", command=select_table_and_continue)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    db_select_dialog.update()
    height = db_select_dialog.winfo_height()
    db_select_dialog.geometry(f"{300}x{height}")


def delete_column_dialog(user, password, selected_db):
    global table_combobox

    def select_table_and_continue():
        global table_combobox
        selected_table = table_combobox.get()
        if selected_table:
            show_columns_for_deletion(user, password, selected_db, selected_table)
        else:
            messagebox.showerror("Ошибка", "Выберите таблицу для удаления столбцов")

    delete_column_window = tk.Toplevel(root)
    delete_column_window.title("Удаление столбца")
    delete_column_window.grab_set()

    db_label = tk.Label(delete_column_window, text="Выберите базу данных:")
    db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(delete_column_window, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)
    db_combobox.insert(0, selected_db)

    table_combobox = ttk.Combobox(delete_column_window, state="readonly")
    table_combobox.grid(row=1, column=1, padx=5, pady=5)

    select_table_button = tk.Button(delete_column_window, text="Выбрать таблицу", command=select_table_and_continue)
    select_table_button.grid(row=1, column=0, padx=5, pady=5)

    delete_column_window.update()
    height = delete_column_window.winfo_height()
    delete_column_window.geometry(f"{300}x{height}")


def choose_table_for_deletion(user, password, selected_db):
    def select_table_and_continue():
        selected_table = table_combobox.get()
        if selected_table:
            show_columns_for_deletion(user, password, selected_db, selected_table)
        else:
            messagebox.showerror("Ошибка", "Выберите таблицу для удаления столбцов")

    choose_table_window = tk.Toplevel(root)
    choose_table_window.title("Выбор таблицы")
    choose_table_window.grab_set()

    table_label = tk.Label(choose_table_window, text="Выберите таблицу:")
    table_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    table_combobox = ttk.Combobox(choose_table_window, state="readonly")
    table_combobox.grid(row=0, column=1, padx=5, pady=5)

    table_list = get_table_list(user, password, selected_db)
    table_combobox['values'] = table_list

    select_table_button = tk.Button(choose_table_window, text="Выбрать", command=select_table_and_continue)
    select_table_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    choose_table_window.update()
    height = choose_table_window.winfo_height()
    choose_table_window.geometry(f"{300}x{height}")


def show_columns_for_deletion(user, password, selected_db, selected_table):
    def delete_columns():
        selected_columns = [column for column, var in zip(column_list, column_vars) if var.get()]
        if not selected_columns:
            messagebox.showerror("Ошибка", "Выберите столбцы для удаления")
            return

        try:
            conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
            conn_local = psycopg2.connect(conn_string)
            with conn_local.cursor() as cursor:
                for column in selected_columns:
                    cursor.execute(f"ALTER TABLE {selected_table} DROP COLUMN {column};")
            conn_local.commit()
            conn_local.close()
            messagebox.showinfo("Успех", f"Выбранные столбцы успешно удалены из таблицы '{selected_table}'")
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении столбцов: {e}")
        finally:
            show_columns_window.destroy()

    show_columns_window = tk.Toplevel(root)
    show_columns_window.title("Выбор столбцов для удаления")
    show_columns_window.grab_set()

    column_list = get_column_list(user, password, selected_db, selected_table)
    column_vars = [tk.BooleanVar() for _ in range(len(column_list))]

    for i, column in enumerate(column_list):
        checkbox = ttk.Checkbutton(show_columns_window, text=column, variable=column_vars[i])
        checkbox.grid(row=i, column=0, sticky="w")

    delete_columns_button = tk.Button(show_columns_window, text="Удалить", command=delete_columns)
    delete_columns_button.grid(row=len(column_list), column=0, padx=5, pady=5)

    show_columns_window.update()
    height = show_columns_window.winfo_height()
    show_columns_window.geometry(f"{300}x{height}")


def get_table_list(user, password, selected_db):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        conn_local = psycopg2.connect(conn_string)
        with conn_local.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            table_list = [table[0] for table in cursor.fetchall()]
        conn_local.close()
        return table_list
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {e}")


def get_column_list(user, password, selected_db, selected_table):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        conn_local = psycopg2.connect(conn_string)
        with conn_local.cursor() as cursor:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}';")
            column_list = [column[0] for column in cursor.fetchall()]
        conn_local.close()
        return column_list
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка столбцов: {e}")


def choose_table_and_view(user, password):
    def select_table_and_show(selected_db, table_combobox, choose_table_window):
        selected_table = table_combobox.get()
        if selected_table:
            show_table_contents(user, password, selected_db, selected_table)
            choose_table_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Выберите таблицу для просмотра")

    def select_db_and_continue():
        selected_db = db_combobox.get()
        if selected_db:
            choose_table_window(selected_db)
        else:
            messagebox.showerror("Ошибка", "Выберите базу данных для просмотра таблиц")

    def choose_table_window(selected_db):
        choose_table_window = tk.Toplevel(root)
        choose_table_window.title("Выбор таблицы")
        choose_table_window.grab_set()

        db_label = tk.Label(choose_table_window, text="Выберите таблицу:")
        db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        table_combobox = ttk.Combobox(choose_table_window, state="readonly")
        table_combobox.grid(row=0, column=1, padx=5, pady=5)

        select_table_button = tk.Button(choose_table_window, text="Выбрать", command=lambda: select_table_and_show(selected_db, table_combobox, choose_table_window))
        select_table_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        choose_table_window.update()
        height = choose_table_window.winfo_height()
        choose_table_window.geometry(f"{300}x{height}")

        table_combobox['values'] = get_table_list(user, password, selected_db)

    db_select_dialog = tk.Toplevel(root)
    db_select_dialog.title("Выбор базы данных")
    db_select_dialog.grab_set()

    db_label = tk.Label(db_select_dialog, text="Выберите базу данных:")
    db_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(db_select_dialog, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_db_button = tk.Button(db_select_dialog, text="Выбрать", command=select_db_and_continue)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    db_select_dialog.update()
    height = db_select_dialog.winfo_height()
    db_select_dialog.geometry(f"{300}x{height}")

    db_combobox['values'] = get_database_list(user, password)


def get_database_list(user, password):
    try:
        conn_string = f"host=localhost port=5432 user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                databases = cursor.fetchall()
        return [db[0] for db in databases]
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка баз данных: {e}")


def get_table_list(user, password, selected_db):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cursor.fetchall()
        return [table[0] for table in tables]
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {e}")


def show_table_contents(user, password, selected_db, selected_table):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}'")
                column_names = [col[0] for col in cursor.fetchall()]

                cursor.execute(f"SELECT * FROM {selected_table};")
                table_contents = cursor.fetchall()

        table_contents_window = tk.Toplevel(root)
        table_contents_window.title(f"Содержимое таблицы '{selected_table}'")

        tree = ttk.Treeview(table_contents_window)
        tree["columns"] = column_names
        tree.grid(row=0, column=0, sticky="nsew")

        for col_name in column_names:
            tree.heading(col_name, text=col_name)

        for row in table_contents:
            tree.insert("", "end", values=row)

    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении содержимого таблицы: {e}")


def add_data_to_table(user, password):
    def insert_data(selected_db, selected_table, entries):
        try:
            conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
            with psycopg2.connect(conn_string) as conn:
                with conn.cursor() as cursor:
                    columns = ', '.join(entries.keys())
                    values = tuple(entry.get() for entry in entries.values())
                    placeholders = ', '.join(['%s'] * len(entries))
                    cursor.execute(
                        f"INSERT INTO {selected_table} ({columns}) VALUES ({placeholders})",
                        values
                    )
                    messagebox.showinfo("Успех", "Данные успешно добавлены!")
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {e}")

    def select_table_and_add_data(selected_db, table_combobox):
        selected_table = table_combobox.get()
        if selected_table:
            choose_columns_window(selected_db, selected_table)
        else:
            messagebox.showerror("Ошибка", "Выберите таблицу")

    def select_db_and_continue():
        selected_db = db_combobox.get()
        if selected_db:
            choose_table_window(selected_db)
        else:
            messagebox.showerror("Ошибка", "Выберите базу данных")

    def choose_columns_window(selected_db, selected_table):
        columns_window = tk.Toplevel(add_data_window)
        columns_window.title("Добавление данных")
        columns_window.grab_set()

        tk.Label(columns_window, text=f"Добавление данных в таблицу '{selected_table}'").grid(row=0, column=0,
                                                                                              columnspan=2, padx=5,
                                                                                              pady=5)

        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}'")
                columns = [col[0] for col in cursor.fetchall()]

        entries = {}
        for idx, column in enumerate(columns):
            tk.Label(columns_window, text=column).grid(row=idx + 1, column=0, padx=5, pady=5, sticky="e")
            entry = tk.Entry(columns_window)
            entry.grid(row=idx + 1, column=1, padx=5, pady=5)
            entries[column] = entry

        tk.Button(columns_window, text="Добавить данные",
                  command=lambda: insert_data(selected_db, selected_table, entries)).grid(row=len(columns) + 1,
                                                                                          column=0, columnspan=2,
                                                                                          padx=5, pady=5)

    def choose_table_window(selected_db):
        choose_table_window = tk.Toplevel(add_data_window)
        choose_table_window.title("Выбор таблицы")
        choose_table_window.grab_set()

        tk.Label(choose_table_window, text="Выберите таблицу:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        table_combobox = ttk.Combobox(choose_table_window, state="readonly")
        table_combobox.grid(row=0, column=1, padx=5, pady=5)

        select_table_button = tk.Button(choose_table_window, text="Выбрать",
                                        command=lambda: select_table_and_add_data(selected_db, table_combobox))
        select_table_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        choose_table_window.update_idletasks()
        height = choose_table_window.winfo_height()
        choose_table_window.geometry(f"{300}x{height}")

        table_combobox['values'] = get_table_list(user, password, selected_db)

    add_data_window = tk.Toplevel(root)
    add_data_window.title("Добавление данных")
    add_data_window.grab_set()

    tk.Label(add_data_window, text="Выберите базу данных:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(add_data_window, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_db_button = tk.Button(add_data_window, text="Выбрать", command=select_db_and_continue)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    add_data_window.update_idletasks()
    height = add_data_window.winfo_height()
    add_data_window.geometry(f"{300}x{height}")

    db_combobox['values'] = get_database_list(user, password)


def get_database_list(user, password):
    try:
        conn_string = f"host=localhost port=5432 user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                databases = cursor.fetchall()
        return [db[0] for db in databases]
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка баз данных: {e}")


def get_table_list(user, password, selected_db):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cursor.fetchall()
        return [table[0] for table in tables]
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {e}")


def clear_table_dialog(user, password):
    def clear_selected_tables(selected_db, selected_tables):
        if selected_tables:
            try:
                conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
                with psycopg2.connect(conn_string) as conn:
                    with conn.cursor() as cursor:
                        for table in selected_tables:
                            cursor.execute(f"DELETE FROM {table};")
                messagebox.showinfo("Успех", "Выбранные таблицы успешно очищены!")
            except psycopg2.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при очистке таблиц: {e}")
        else:
            messagebox.showerror("Ошибка", "Выберите хотя бы одну таблицу для очистки")

    def select_tables_and_clear(selected_db, table_checkboxes):
        selected_tables = [table for table, var in table_vars.items() if var.get()]
        clear_selected_tables(selected_db, selected_tables)
        clear_table_window.destroy()

    def select_db_and_continue():
        selected_db = db_combobox.get()
        if selected_db:
            choose_table_window(selected_db)
        else:
            messagebox.showerror("Ошибка", "Выберите базу данных")

    def choose_table_window(selected_db):
        choose_table_window = tk.Toplevel(clear_table_window)
        choose_table_window.title("Выбор таблицы")
        choose_table_window.grab_set()

        tk.Label(choose_table_window, text="Выберите таблицы для очистки:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        for idx, table in enumerate(get_table_list(user, password, selected_db)):
            var = tk.BooleanVar(value=False)
            tk.Checkbutton(choose_table_window, text=table, variable=var).grid(row=idx+1, column=0, padx=5, pady=2, sticky="w")
            table_vars[table] = var

        select_table_button = tk.Button(choose_table_window, text="Выбрать", command=lambda: select_tables_and_clear(selected_db, table_vars))
        select_table_button.grid(row=len(table_vars)+1, column=0, columnspan=2, padx=5, pady=5)

        choose_table_window.update_idletasks()
        height = choose_table_window.winfo_height()
        choose_table_window.geometry(f"{300}x{height}")

    clear_table_window = tk.Toplevel(root)
    clear_table_window.title("Очистка таблицы")
    clear_table_window.grab_set()

    table_vars = {}

    tk.Label(clear_table_window, text="Выберите базу данных:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(clear_table_window, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_db_button = tk.Button(clear_table_window, text="Выбрать", command=select_db_and_continue)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    clear_table_window.update_idletasks()
    height = clear_table_window.winfo_height()
    clear_table_window.geometry(f"{300}x{height}")

    db_combobox['values'] = get_database_list(user, password)


def edit_data_dialog(user, password):
    def select_row_and_edit(selected_db, selected_table, row_combobox):
        selected_row_data_list = row_combobox.get()

        if selected_row_data_list:
            edit_data_in_row(selected_db, selected_table, user, password, selected_row_data_list)
        else:
            messagebox.showerror("Ошибка", "Выберите строку для редактирования")

    def select_table_and_show_rows(selected_db, table_combobox):
        selected_table = table_combobox.get()

        if selected_table:
            choose_row_window(user, password, selected_db, selected_table)
        else:
            messagebox.showerror("Ошибка", "Выберите таблицу")

    def select_db_and_continue():
        selected_db = db_combobox.get()

        if selected_db:
            choose_table_window(user, password, selected_db)
        else:
            messagebox.showerror("Ошибка", "Выберите базу данных")

    def choose_row_window(user, password, selected_db, selected_table):
        choose_row_window = tk.Toplevel(edit_data_window)
        choose_row_window.title("Выбор строки")
        choose_row_window.grab_set()

        tk.Label(choose_row_window, text="Выберите строку для редактирования:").grid(row=0, column=0, padx=5, pady=5,
                                                                                     sticky="e")

        row_combobox = ttk.Combobox(choose_row_window, state="readonly")
        row_combobox.grid(row=0, column=1, padx=5, pady=5)

        select_row_button = tk.Button(choose_row_window, text="Выбрать",
                                      command=lambda: select_row_and_edit(selected_db, selected_table, row_combobox))
        select_row_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        choose_row_window.update_idletasks()
        height = choose_row_window.winfo_height()
        choose_row_window.geometry(f"{400}x{height}")

        rows = get_rows_list(user, password, selected_db, selected_table)
        row_combobox['values'] = rows

    def get_columns_list(user, password, selected_db, selected_table):
        try:
            conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
            with psycopg2.connect(conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}'")
                    columns = cursor.fetchall()
                    return [column[0] for column in columns]
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении списка столбцов: {e}")
            return []

    def edit_data_in_row(selected_db, selected_table, user, password, selected_row_data):
        selected_row_data_list = selected_row_data.split()
        columns = get_columns_list(user, password, selected_db, selected_table)

        if len(columns) != len(selected_row_data_list):
            messagebox.showerror("Ошибка",
                                 "Количество выбранных значений не совпадает с количеством столбцов в таблице.")
            return

        selected_row_data_dict = dict(zip(columns, selected_row_data_list))

        edit_data_in_row_window = tk.Toplevel(edit_data_window)
        edit_data_in_row_window.title("Редактирование данных")
        edit_data_in_row_window.grab_set()

        tk.Label(edit_data_in_row_window, text=f"Редактирование данных в строке таблицы '{selected_table}'").grid(row=0,
                                                                                                                  column=0,
                                                                                                                  columnspan=2,
                                                                                                                  padx=5,
                                                                                                                  pady=5)

        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                condition = " AND ".join([f"{column} = %s" for column in selected_row_data_dict.keys()])
                cursor.execute(f"SELECT * FROM {selected_table} WHERE {condition}",
                               tuple(selected_row_data_dict.values()))
                row_data = cursor.fetchone()

                if row_data:
                    entries = {}
                    for idx, column in enumerate(columns):
                        tk.Label(edit_data_in_row_window, text=column).grid(row=idx + 1, column=0, padx=5, pady=5,
                                                                            sticky="e")
                        entry = tk.Entry(edit_data_in_row_window)
                        entry.insert(0, row_data[idx])  # Заполняем поля ввода старыми данными
                        entry.grid(row=idx + 1, column=1, padx=5, pady=5)
                        entries[column] = entry

                    def update_data():
                        try:
                            new_values = tuple(entry.get() for entry in entries.values())
                            set_clause = ', '.join([f"{col} = %s" for col in columns])
                            condition = " AND ".join([f"{column} = %s" for column in selected_row_data_dict.keys()])
                            condition_values = tuple(selected_row_data_dict.values())

                            conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
                            with psycopg2.connect(conn_string) as conn:
                                with conn.cursor() as cursor:
                                    cursor.execute(f"UPDATE {selected_table} SET {set_clause} WHERE {condition}",
                                                   new_values + condition_values)
                                    conn.commit()
                                    messagebox.showinfo("Успех", "Данные успешно обновлены!")
                                    edit_data_in_row_window.destroy()
                        except psycopg2.Error as e:
                            messagebox.showerror("Ошибка", f"Ошибка при обновлении данных: {e}")

                    tk.Button(edit_data_in_row_window, text="Обновить данные", command=update_data).grid(
                        row=len(columns) + 1, column=0, columnspan=2, padx=5, pady=5)

                else:
                    messagebox.showerror("Ошибка",
                                         f"Строка с данными {selected_row_data} не найдена в таблице '{selected_table}'")

    def choose_table_window(user, password, selected_db):
        choose_table_window = tk.Toplevel(edit_data_window)
        choose_table_window.title("Выбор таблицы")
        choose_table_window.grab_set()

        tk.Label(choose_table_window, text="Выберите таблицу:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        table_combobox = ttk.Combobox(choose_table_window, state="readonly")
        table_combobox.grid(row=0, column=1, padx=5, pady=5)

        select_table_button = tk.Button(choose_table_window, text="Выбрать",
                                        command=lambda: select_table_and_show_rows(selected_db, table_combobox))
        select_table_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        choose_table_window.update_idletasks()
        height = choose_table_window.winfo_height()
        choose_table_window.geometry(f"{300}x{height}")

        tables = get_table_list(user, password, selected_db)
        table_combobox['values'] = tables

    edit_data_window = tk.Toplevel(root)
    edit_data_window.title("Редактирование данных")
    edit_data_window.grab_set()

    tk.Label(edit_data_window, text="Выберите базу данных:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(edit_data_window, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_db_button = tk.Button(edit_data_window, text="Выбрать", command=select_db_and_continue)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    edit_data_window.update_idletasks()
    height = edit_data_window.winfo_height()
    edit_data_window.geometry(f"{300}x{height}")

    db_combobox['values'] = get_database_list(user, password)


def get_rows_list(user, password, selected_db, selected_table):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {selected_table};")
                rows = cursor.fetchall()
        return rows
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка строк: {e}")


def search_data_dialog(user, password):
    choose_db_for_search(user, password)


def choose_db_for_search(user, password):
    choose_db_window = tk.Toplevel(root)
    choose_db_window.title("Выбор базы данных")
    choose_db_window.grab_set()

    tk.Label(choose_db_window, text="Выберите базу данных:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    db_combobox = ttk.Combobox(choose_db_window, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_db_button = tk.Button(choose_db_window, text="Выбрать", command=lambda: choose_table_for_search(user, password, db_combobox.get()), width=10)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    choose_db_window.update_idletasks()
    height = choose_db_window.winfo_height()
    choose_db_window.geometry(f"{300}x{height}")

    db_combobox['values'] = get_database_list(user, password)


def choose_table_for_search(user, password, selected_db):
    choose_table_window = tk.Toplevel(root)
    choose_table_window.title("Выбор таблицы для поиска")
    choose_table_window.grab_set()

    tk.Label(choose_table_window, text="Выберите таблицу:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    table_combobox = ttk.Combobox(choose_table_window, state="readonly")
    table_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_table_button = tk.Button(choose_table_window, text="Выбрать", command=lambda: select_column_for_search(user, password, selected_db, table_combobox.get()), width=10)
    select_table_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    choose_table_window.update_idletasks()
    height = choose_table_window.winfo_height()
    choose_table_window.geometry(f"{300}x{height}")

    table_combobox['values'] = get_table_list(user, password, selected_db)


def select_column_for_search(user, password, selected_db, selected_table):
    select_column_window = tk.Toplevel(root)
    select_column_window.title("Выбор столбца для поиска")
    select_column_window.grab_set()

    tk.Label(select_column_window, text="Выберите столбец:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    column_combobox = ttk.Combobox(select_column_window, state="readonly")
    column_combobox.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(select_column_window, text="Введите значение для поиска:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

    value_entry = tk.Entry(select_column_window)
    value_entry.grid(row=1, column=1, padx=5, pady=5)

    select_column_button = tk.Button(select_column_window, text="Выбрать", command=lambda: select_column_and_search(user, password, selected_db, selected_table, column_combobox.get(), value_entry.get()), width=10)
    select_column_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    select_column_window.update_idletasks()
    height = select_column_window.winfo_height()
    select_column_window.geometry(f"{350}x{height}")

    column_combobox['values'] = get_columns_list(user, password, selected_db, selected_table)


def get_columns_list(user, password, selected_db, selected_table):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}'")
                columns = cursor.fetchall()
                return [column[0] for column in columns]
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка столбцов: {e}")
        return []


def select_column_and_search(user, password, selected_db, selected_table, selected_column, value_to_search):
    if not value_to_search:
        messagebox.showerror("Ошибка", "Введите значение для поиска")
        return

    search_results = search_data_in_column(user, password, selected_db, selected_table, selected_column, value_to_search)

    if search_results:
        show_search_results(search_results)
    else:
        messagebox.showinfo("Результат поиска", "Ничего не найдено")


def search_data_in_column(user, password, selected_db, selected_table, selected_column, value_to_search):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {selected_table} WHERE {selected_column} = %s", (value_to_search,))
                rows = cursor.fetchall()
        return rows
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при поиске данных: {e}")
        return []


def show_search_results(search_results):
    search_results_window = tk.Toplevel()
    search_results_window.title("Результаты поиска")

    search_results_window.grab_set()

    tree = ttk.Treeview(search_results_window)
    tree["columns"] = tuple(range(len(search_results[0])))
    tree["show"] = "headings"

    for row in search_results:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")


def delete_data_dialog(user, password):
    choose_db_for_deletion1(user, password)


def choose_db_for_deletion1(user, password):
    def choose_table_for_deletion(selected_db):
        choose_table_window = tk.Toplevel(root)
        choose_table_window.title("Выбор таблицы для удаления")
        choose_table_window.grab_set()

        tk.Label(choose_table_window, text="Выберите таблицу:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        table_combobox = ttk.Combobox(choose_table_window, state="readonly")
        table_combobox.grid(row=0, column=1, padx=5, pady=5)

        select_table_button = tk.Button(choose_table_window, text="Выбрать", command=lambda: select_column_for_deletion(user, password, selected_db, table_combobox.get()), width=10)
        select_table_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        choose_table_window.update_idletasks()
        height = choose_table_window.winfo_height()
        choose_table_window.geometry(f"{300}x{height}")

        table_combobox['values'] = get_table_list(user, password, selected_db)

    choose_db_window = tk.Toplevel(root)
    choose_db_window.title("Выбор базы данных для удаления")
    choose_db_window.grab_set()

    tk.Label(choose_db_window, text="Выберите базу данных:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    db_combobox = ttk.Combobox(choose_db_window, state="readonly")
    db_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_db_button = tk.Button(choose_db_window, text="Выбрать", command=lambda: choose_table_for_deletion(db_combobox.get()), width=10)
    select_db_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    choose_db_window.update_idletasks()
    height = choose_db_window.winfo_height()
    choose_db_window.geometry(f"{300}x{height}")

    db_combobox['values'] = get_database_list(user, password)


def select_column_for_deletion(user, password, selected_db, selected_table):
    select_column_window = tk.Toplevel(root)
    select_column_window.title("Выбор столбца для удаления")
    select_column_window.grab_set()

    tk.Label(select_column_window, text="Выберите столбец:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    column_combobox = ttk.Combobox(select_column_window, state="readonly")
    column_combobox.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(select_column_window, text="Введите значение для удаления:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    value_entry = tk.Entry(select_column_window)
    value_entry.grid(row=1, column=1, padx=5, pady=5)

    delete_button = tk.Button(select_column_window, text="Удалить", command=lambda: delete_rows_by_value(user, password, selected_db, selected_table, column_combobox.get(), value_entry.get()), width=10)
    delete_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    select_column_window.update_idletasks()
    height = select_column_window.winfo_height()
    select_column_window.geometry(f"{350}x{height}")

    column_combobox['values'] = get_columns_list(user, password, selected_db, selected_table)


def delete_rows_by_value(user, password, selected_db, selected_table, selected_column, value_to_delete):
    try:
        conn_string = f"host=localhost port=5432 dbname={selected_db} user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"DELETE FROM {selected_table} WHERE {selected_column} = %s", (value_to_delete,))
        messagebox.showinfo("Удаление", f"Успешно удалены строки из таблицы '{selected_table}' по значению '{value_to_delete}' в столбце '{selected_column}'")
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении данных: {e}")


def create_role(user, password, role_name, role_password, create_db=False, allow_login=False, superuser=False,
                create_roles=False, inherit=False, replication=False, bypass_rls=False):
    try:
        conn_string = f"host=localhost port=5432 dbname=postgres user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                # Создание пользователя с указанным именем и паролем
                cursor.execute(f"CREATE USER {role_name} WITH PASSWORD '{role_password}'")

                # Назначение прав роли
                cursor.execute(f"ALTER USER {role_name} {'CREATEDB' if create_db else 'NOCREATEDB'}")
                cursor.execute(f"ALTER USER {role_name} {'LOGIN' if allow_login else 'NOLOGIN'}")
                cursor.execute(f"ALTER USER {role_name} {'SUPERUSER' if superuser else 'NOSUPERUSER'}")
                cursor.execute(f"ALTER USER {role_name} {'CREATEROLE' if create_roles else 'NOCREATEROLE'}")
                cursor.execute(f"ALTER USER {role_name} {'INHERIT' if inherit else 'NOINHERIT'}")
                cursor.execute(f"ALTER USER {role_name} {'REPLICATION' if replication else 'NOREPLICATION'}")
                cursor.execute(f"ALTER USER {role_name} {'BYPASSRLS' if bypass_rls else 'NOBYPASSRLS'}")

        messagebox.showinfo("Успех", f"Роль {role_name} успешно создана!")

    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при создании роли: {e}")


def get_roles_list(user, password):
    roles_list = []
    try:
        conn_string = f"host=localhost port=5432 dbname=postgres user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT rolname FROM pg_roles WHERE rolname != 'postgres' AND rolname != 'pg_signal_backend'")
                roles_list = [row[0] for row in cursor.fetchall()]
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка ролей: {e}")
    return roles_list


def delete_role(user, password, role):
    try:
        conn_string = f"host=localhost port=5432 dbname=postgres user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"DROP ROLE {role}")
        messagebox.showinfo("Успех", f"Роль {role} успешно удалена!")
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении роли {role}: {e}")

def get_permissions(user, password, role):
    permissions_list = []
    try:
        conn_string = f"host=localhost port=5432 dbname=postgres user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT rolcreatedb, rolcanlogin, rolsuper, rolcreaterole, rolinherit, rolreplication, rolbypassrls FROM pg_roles WHERE rolname = '{role}'")
                permissions = cursor.fetchone()
                if permissions:
                    if permissions[0]:
                        permissions_list.append("CREATEDB")
                    if permissions[1]:
                        permissions_list.append("LOGIN")
                    if permissions[2]:
                        permissions_list.append("SUPERUSER")
                    if permissions[3]:
                        permissions_list.append("CREATEROLE")
                    if permissions[4]:
                        permissions_list.append("INHERIT")
                    if permissions[5]:
                        permissions_list.append("REPLICATION")
                    if permissions[6]:
                        permissions_list.append("BYPASSRLS")
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении прав роли: {e}")
    return permissions_list


def get_roles_list(user, password):
    roles = []
    try:
        conn_string = f"host=localhost port=5432 dbname=postgres user={user} password={password}"
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT rolname FROM pg_roles WHERE rolname !~ '^pg_' AND rolname <> 'postgres'")
                roles = [row[0] for row in cursor.fetchall()]
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка ролей: {e}")
    return roles


def change_permissions(user, password, role, new_username, new_password, new_permissions):
    global conn
    try:
        if role.lower() != "postgres":
            conn_string = f"host=localhost port=5432 dbname=postgres user={user} password={password}"
            with psycopg2.connect(conn_string) as conn:
                with conn.cursor() as cursor:
                    if new_username:
                        cursor.execute(f"ALTER ROLE {role} RENAME TO {new_username}")
                        role = new_username
                    if new_password:
                        cursor.execute(f"ALTER ROLE {role} WITH PASSWORD '{new_password}'")

                    cursor.execute(f"ALTER ROLE {role} {'CREATEDB' if new_permissions['CREATEDB'] else 'NOCREATEDB'}")
                    cursor.execute(f"ALTER ROLE {role} {'LOGIN' if new_permissions['LOGIN'] else 'NOLOGIN'}")
                    cursor.execute(
                        f"ALTER ROLE {role} {'SUPERUSER' if new_permissions['SUPERUSER'] else 'NOSUPERUSER'}")
                    cursor.execute(
                        f"ALTER ROLE {role} {'CREATEROLE' if new_permissions['CREATEROLE'] else 'NOCREATEROLE'}")
                    cursor.execute(f"ALTER ROLE {role} {'INHERIT' if new_permissions['INHERIT'] else 'NOINHERIT'}")
                    cursor.execute(
                        f"ALTER ROLE {role} {'REPLICATION' if new_permissions['REPLICATION'] else 'NOREPLICATION'}")
                    cursor.execute(
                        f"ALTER ROLE {role} {'BYPASSRLS' if new_permissions['BYPASSRLS'] else 'NOBYPASSRLS'}")

            messagebox.showinfo("Успех", f"Права роли {role} успешно изменены!")
            with psycopg2.connect(conn_string) as conn:
                pass
        else:
            messagebox.showwarning("Предупреждение", "Выбранная роль не может быть системной ролью.")
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при изменении прав роли: {e}")


def main():
    global root, username_entry, password_entry

    root = tk.Tk()
    root.title("Подключение к базе данных")

    default_user = "login"
    default_password = "password"

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    username_label = tk.Label(root, text="Логин:")
    username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    username_entry = tk.Entry(root)
    username_entry.insert(0, default_user)
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    password_label = tk.Label(root, text="Пароль:")
    password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    password_entry = tk.Entry(root, show="*")
    password_entry.insert(0, default_password)
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    connect_button = tk.Button(root, text="Подключиться", command=connect_to_database)
    connect_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    root.update()
    height = root.winfo_height()
    root.geometry(f"{300}x{height}")
    root.mainloop()


if __name__ == "__main__":
    main()
