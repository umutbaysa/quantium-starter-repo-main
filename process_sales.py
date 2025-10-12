import pandas as pd


def process_pink_morsel_sales():
    
    df1 = pd.read_csv('data/daily_sales_data_0.csv')
    df2 = pd.read_csv('data/daily_sales_data_1.csv')
    df3 = pd.read_csv('data/daily_sales_data_2.csv')


    all_data = pd.concat([df1, df2, df3], ignore_index=True)

    pink_data = all_data[all_data['product'].str.lower() == 'pink morsel'].copy()

    # Remove $ sign and convert price to float
    pink_data['price_clean'] = pink_data['price'].str.replace('$', '', regex=False).astype(float)
    pink_data['sales'] = pink_data['quantity'] * pink_data['price_clean']

    pink_data['date'] = pd.to_datetime(pink_data['date'])

    final_data = pink_data[['sales', 'date', 'region']].copy()
    final_data.columns = ['Sales', 'Date', 'Region']


    output_path = 'data/pink_morsel_sales.csv'
    final_data.to_csv(output_path, index=False)

    print(f"✅ Process completed! Output file saved to: {output_path}")
    print(f"\nSummary:")
    print(f"  Total Pink Morsel records: {len(final_data):,}")
    print(f"  Total sales: ${final_data['Sales'].sum():,.2f}")


if __name__ == "__main__":
    process_pink_morsel_sales()
