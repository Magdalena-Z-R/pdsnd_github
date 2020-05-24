import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington).
    cities = ['chicago', 'new york city', 'washington']
    city = str(input('Would you like to see data for Chicago, New York City, or Washington? ')).lower()
    while city not in cities:
        city = str(input('Please write city filter: Chicago, New York City, or Washington ')).lower()

    #get filter for the data by month, day, or not at all
    filters = ['all', 'month', 'day']
    filter = str(input('Would you like to filter the data by month, day, or not at all? Type "all" for no time filter. ')).lower()
    while filter not in filters:
        filter = str(input('Please write filter: month, day, or none.  ')).lower()

    month = 'all'
    day = 'all'
    #get user input for month (all, january, february, ... , june)
    if filter == 'month':
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = str(input('Which month - January, February, March, April, May, or June? ')).lower()
        while month not in months:
            month = str(input('Please write month filter: January, February, March, April, May, or June ')).lower()

    #get user input for day of week (all, monday, tuesday, ... sunday)
    elif filter == 'day':
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = str(input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ')).lower()
        while day not in days:
            day = str(input('Please write day filter: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday ')).lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df['month'].mode()[0]
    print('The most popular month is', most_popular_month)

    # display the most common day of week
    most_popular_weekday_name = df['day_of_week'].mode()[0]
    print('The most popular day of the week is ', most_popular_weekday_name)

    # display the most common start hour
    most_popular_hour = df['hour'].mode()[0]
    print('The most popular hour is', most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('The most cocommonly used start station is', most_popular_start_station)

    # display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is', most_popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start_End'] = df['Start Station'] + ' - ' + df['End Station']
    most_popular_start_end_combination = df['Start_End'].mode()[0]
    print('The most frequent combination of start station and end station trip is:', most_popular_start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('counts of user types:', user_types)

    if "Gender" in df.columns:
        # Display counts of gender
        user_gender = df['Gender'].value_counts()
        print('User gender counts: ', user_gender)
        # Display earliest year of birth
        earliest_yob = df['Birth Year'].min()
        print('The earliest year of birth:', earliest_yob)
        # Display most recent year of birth
        recent_yof = df['Birth Year'].max()
        print('The most recent year of birth:', recent_yof)
        # Display most common year of birth
        common_yob = df['Birth Year'].mode()[0]
        print('The most common year of birth:', common_yob )

    else:
        print('We do not have user gender and year of birth data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display some raw data if applicable
        start = 0
        count = 5
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        while raw_data.lower() == 'yes':
            print('Some raw data', df.iloc[start : count])
            raw_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
            count +=5
            start +=5


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
