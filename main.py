from pyspark.sql import SparkSession
from pyspark.sql.functions import desc

# Now instantiate your spark session using builder..
spark = SparkSession.builder.master("local").appName("myapp").getOrCreate()


def get_product_category_pairs_with_no_category(df_product, df_category, df_matches):

    # делаем inner join для пересечений и категорий
    df_joined_category = df_matches.join(df_category, df_category.CategoryID == df_matches.CategoryID, "inner")

    # делаем left join для продуктов и пересечений, что бы включить продукты без категорий
    # включим в содержание нового DataFrame-а только ProductName и CategoryName колонки
    # Отсортируем по категориям в порядке убывания
    df_joined_category_product = df_product.join(df_joined_category,
                                                 df_product.ProductID == df_joined_category.ProductID, "left")\
                                            .select(df_product.ProductName, df_joined_category.CategoryName)\
                                            .sort(desc(df_joined_category.CategoryName))

    return df_joined_category_product


def main():
    # из созданных csv создаём DataFrame-ы
    df_product = spark.read.option("delimiter", ";").option("header", True).csv("product.csv")
    df_category = spark.read.option("delimiter", ";").option("header", True).csv("category.csv")
    df_matches = spark.read.option("delimiter", ";").option("header", True).csv("matches.csv")
    # выведем датафреймы на экран
    print(df_product.show(100), df_category.show(100), df_matches.show(100))

    df_merged = get_product_category_pairs_with_no_category(df_product, df_category, df_matches)
    print(df_merged.show(100))


if __name__ == '__main__':
    main()
