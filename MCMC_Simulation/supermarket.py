"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""
Markov Chain Montecarlo Simulator of the daily customer flux in a supermarket
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# import built-in libraries
import os
import datetime as dt
import time
from colorama import Fore, Style, init

init()
import logging

logging.basicConfig(level=logging.WARNING, format="%(message)s")

# import other libraries
import numpy as np
import pandas as pd
from faker import Faker
from pyfiglet import Figlet

# import scripts
import proba


class Customer:
    """
    a single customer that moves through the supermarket
    in a MCMC simulation
    """

    def __init__(self, name, state="entrance", budget=100):
        self.name = name
        self.state = state
        self.budget = budget

    def __repr__(self):
        return f"{self.name} is in {self.state}."


    def next_state(self):
        """
        Propagates the customer to the next state.
        Returns nothing.
        """
        # WARNING: CHECK THE ORDER OF THE AISLES WHEN THE ACTUAL MATRIX ARRIVES
        aisles = ["checkout", "dairy", "drinks", "fruit", "spices"]

        if self.state in aisles:

            if self.state == "dairy":
                initial_state = np.array([0.0, 1.0, 0.0, 0.0, 0.0])
            elif self.state == "drinks":
                initial_state = np.array([0.0, 0.0, 1.0, 0.0, 0.0])
            elif self.state == "fruit":
                initial_state = np.array([0.0, 0.0, 0.0, 1.0, 0.0])
            elif self.state == "spices":
                initial_state = np.array([0.0, 0.0, 0.0, 0.0, 1.0])
            elif self.state == "checkout":
                initial_state = np.array([1.0, 0.0, 0.0, 0.0, 0.0])

            next_state_prob = np.dot(initial_state, proba.prob)

            self.state = np.random.choice(aisles, p=next_state_prob)

        else:
            self.state = np.random.choice(
                ["spices", "drinks", "fruit", "dairy"], p=proba.ent_prob
            )

    def is_active(self):
        """Returns True if the customer has not reached the checkout yet."""
        if self.state == "checkout":
            return False
        else:
            return True


class SuperMarket:
    """manages multiple Customer instances that are currently in the market."""

    def __init__(self):
        """a list of Customer objects"""
        self.customers = []
        self.minutes = dt.datetime(today.year, today.month, today.day, 6, 50)
        # self.last_id = 0
        self.state = "closed"

    def __repr__(self):
        return (
            Fore.CYAN
            + f"\n{self.minutes} – The supermarket is {self.state}: currently, there are {len(self.customers)} customers inside.\n"
            + Style.RESET_ALL
        )

    def get_time(self):
        """opens and closes the supermarket,
        and pushes customers to the checkout,
        """

        if (
            self.minutes.hour > 22
            or self.minutes.hour <= 6
            and self.minutes.minute <= 59
        ):
            logging.warning(
                f"{self.minutes} - The supermarket is closed. It will reopen at 7 AM."
            )

        elif self.minutes.hour == 22 and self.minutes.minute == 0:
            logging.warning(
                Fore.RED
                + f"{self.minutes} - The supermarket has closed."
                + Style.RESET_ALL
            )

            self.state = "closed"

        elif self.minutes.hour == 21 and self.minutes.minute == 57:
            for cust in self.customers:
                if cust.is_active() == True:
                    cust.state = "checkout"

        elif self.minutes.hour == 7 and self.minutes.minute == 0:
            logging.warning(
                Fore.GREEN
                + f"{self.minutes} - The supermarket has opened its doors!\n"
                + Style.RESET_ALL
            )
            self.state = "open"

        else:
            self.state = "open"

        return None

    def add_new_customers(self):
        """generate new customers at their initial location based on the fluxes illustrated in the EDA."""
        if (
            self.minutes.hour >= 22
            or self.minutes.hour <= 6
            and self.minutes.minute <= 59
        ):
            pass
        else:
            tm = str(self.minutes)[-8:]
            try:
                cust_no = int(proba.entrance_number.loc[tm])
            except:
                cust_no = 0
            for cust in range(cust_no):
                c = Customer(f.name())
                logging.warning(
                    Fore.YELLOW
                    + f"{self.minutes} - {c.name} has entered the supermarket."
                    + Style.RESET_ALL
                )
                self.customers.append(c)

        return None

    def next_minute(self):
        """increase the time of the supermarket by one minute,
        propagates all customers to the next state.
        """
        self.minutes = self.minutes + dt.timedelta(minutes=1)
        if self.minutes.hour in [i for i in range(0, 24)] and self.minutes.minute == 0:
            logging.warning(self)

        for cust in self.customers:
            cust.next_state()
            logging.warning(f"{self.minutes} – {cust}")

        return None

    def remove_exiting_customers(self):
        """removes every customer that is not active any more."""
        for cust in self.customers:
            if cust.is_active() == False:
                logging.warning(
                    Fore.BLUE
                    + f"{self.minutes} - {cust.name} has left the supermarket."
                    + Style.RESET_ALL
                )
                self.customers.remove(cust)

        return None

    def record_customers(self):
        """append the state of different customers to a log DataFrame."""
        df = pd.DataFrame(columns=["time", "customer", "location"])
        for cust in self.customers:
            if cust.state == "checkout":
                final_st = "checkout and leave"
            else:
                final_st = cust.state
            row = pd.DataFrame(
                data=[str(self.minutes)[-8:], cust.name, final_st],
                index=["time", "customer", "location"],
            ).transpose()
            df = pd.concat([df, row], ignore_index=True)

        return df


if __name__ == "__main__":

    # output DataFrame
    record = pd.DataFrame(columns=["time", "customer", "location"])

    # Taking the current date and hour
    today = dt.date.today()
    now = dt.datetime.now().strftime("%Hh%M")

    # Name faker
    f = Faker()

    # Class instatiation
    s = SuperMarket()

    # title
    logging.warning(Figlet().renderText("One Day at the Supermarket\n"))
    logging.warning(
        "This is a Markov Chain Montecarlo simulator of a supermarket over a single working day (7:00-22:00).\nThe simulation will start in a few seconds...\n"
    )

    # Loop
    for i in range(920):
        s.get_time()
        s.add_new_customers()
        df = s.record_customers()
        record = pd.concat([record, df], ignore_index=True)
        s.remove_exiting_customers()
        s.next_minute()

        time.sleep(0.2)

    # output file
    path = "output"
    if not os.path.exists(path):
        os.makedirs(path)
    record.to_csv(f"output/MCMCsim_supermarket_{today}_{now}.csv", sep=";")
    logging.warning(
        f"Run this script again if you wish to run another MC simulation.\nThe file 'MCMCsim_supermarket_{today}_{now}.csv' that contains the data of this simulation is now available in the output folder.\n"
    )
