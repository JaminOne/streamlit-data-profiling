import streamlit as st
import snowflake.connector
import pandas as pd
# from credentials import sf_credentials

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"],insecure_mode=True, ocsp_fail_open=False)   
con = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# @st.experimental_memo(ttl=600)
# def run_query(query):
#     with con.cursor() as cur:
#         cur.execute(query)
#         return cur.fetch_pandas_all()
st.title("❄️Data Profiling Dashboard")
st.write("#### ❄️Table Address:")

db_name = st.text_input("Enter Snowflake Database Name", "JAMIN_TEST", type = "default")
schema_name = st.text_input("Enter Snowflake Schema Name", "PUBLIC", type = "default")
table_name = st.text_input("Enter Snowflake Table Name", "SALES", type = "default")

query_table_name = f"{db_name}.{schema_name}.{table_name}"

if query_table_name:
    # sf_table = "JAMIN_TEST.PUBLIC.SALES_TALEND_CREATE"
    # df = run_query(query)
    query = f"SELECT * FROM {query_table_name}"
    query_text = f'<p style="font-family:sans-serif; color:Green; font-size: 15px;">Executed Query: {query}</p>'
    st.markdown(query_text, unsafe_allow_html=True)
    # exception for inputing wrong table name
    try:
        df = pd.read_sql(query, con)
    except Exception as e:
        st.warning("Entered wrong table")
        st.stop()
   
    # building streamlit app
    st.write("#### Table Preview:")
    st.write(df.head())

    # length of the table
    columns_length = len(df.columns)
    row_length = len(df)

    # shape
    st.write(f"Table has {columns_length} columns * {row_length} rows")

    # table status
    st.write("#### Table Status")
    st.write(df.describe(include="all").fillna("").astype("str"))

    st.write("#### Null Value")
    st.write(df.isnull().sum())

    st.write("#### Duplicate Row")
    st.write("Table has", df.duplicated().sum(), " duplicated rows")
    st.write(df[df.duplicated()])


    # distribution graph
    st.write("#### Distribution Graph for All Categorical Cols")
    col_list = df.select_dtypes(include="object_").columns
    for col in col_list:
        st.bar_chart(df[col].value_counts())

else:
    st.warning('Please Input a Valid Table Name')