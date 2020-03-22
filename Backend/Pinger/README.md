# Pinger Library

The Pinger is a library which can:
1. Upload a list of DNA-Sequences to multiple vendors
2. Receive offers with price and turnover time for various dna-sequences
3. Create a shopping cart with different offers

Hint: Not every vendor provides all of these functions via their APIs. And in most cases you need a technical account. Default customers often have no access.

## Installation

You can find a `setup.py` in the `Backend` directory. With this file you can install the dnabackend resources with:
```bash
pip3 install /path/to/projectfolder/Backend/
```

If an error occurs you maybe need to be root user. Sometimes `sudo` is not enough so run `sudo su` to login as root user.

If the command runs successfully Pinger-Library is installed.

## Structure

The Pinger Library has three parts:
1. A static part: It contains only classes which define the structure of objects passed to the pinger and returned from the pinger. You can find it in the file `Entities.py`.
2. An interactive part: This is the part where the user can do the actions. The user have to initialize an instance of a pinger and can register the different vendors he needs. You can find it in the file `Pinger.py`.
3. A vendor specific part: This is the part of the implementations for specific vendors. Every vendor has a different API and thats why every vendor has to be implemented once.

## How to use

It's recommended that you take a short look at `Entities.py` and `Pinger.py` before continuing.

```python
# import static and interactive part
from Pinger import Pinger, Entities

# Initialize a managed Pinger
pinger = Pinger.CompositePinger()
```

The first example is simple. We import the resources and initialize a managed Pinger. Maybe you ask yourself what is a *managed* Pinger. 

We have two kinds of Pingers:
1.  Base Pinger
2.  Managed Pinger

A Base Pinger represents a specific vendor, we often call it Vendor-Pinger. So if you want to implement a new Vendor then you have to implement a Base Pinger which uses the API of the new vendor. 
A Managed Pinger handles multiple Base-Pingers to spread the pinger-actions to multiple vendors with one call. It aggregates the result und you can filter on specific vendors.

```python
# import static and interactive part
from Pinger import Pinger, Entities, FictionalVendor

# Initialize a managed Pinger
pinger = Pinger.CompositePinger()

# Initialize the Vendor-Pinger of a specfific vendor
fictional_vendor_pinger = FictionalVendor.VendorPinger("username", "password", "base_url")

# Create your representation of the vendor
fictional_vendor_info = Entities.VendorInformation(name="Fictional vendor GmbH", shortName="Vendor", key=1)

# Register the vendor at your managed Pinger
pinger.registerVendor(fictional_vendor_info, fictional_vendor_pinger)
```

Now we have extend the code. We import a vendor out of the Pinger Library. This is a fictional vendor, you have to use a real available vendor. Currently folder contains Python-Files which have the same name as a real vendor. These files contain implementations of the BasePinger Class. This implementation is what we instantiate as `fictional_vendor_pinger`. (That's the third part: vendor specific part)

Every vendor has diffent credentials with different forms, that's why the initialization of the vendor pingers are not uniform. All the other actions are uniform.

After creating an instance of a Vendor-Pinger it's the first time we have to use the static part. We create an instance of the entity `VendorInformation`. It represents a vendor. As also stated in `Entities.py`, it is important to use an unique id. The vendor names are for the user for easy reading and better output/error-messages.

At last we can register this vendor with the pinger and the information object by calling registerVendor. 

You can register as many Vendors as you want.

Now you can use the managed Pinger to search for offers for a specific sequence as shown in the following example:

```python
# Sequences to search for offers
sequences = [Entities.SequenceInformation("ACTG", "TestSequence", "sequence_1")]

# Start searching for a sequence
pinger.searchOffers(sequences)

# Wait the requests to finish
while pinger.isRunning():
    pass

# Get the result
offers = pinger.getOffers()

print(offers[0].vendorOffers[0].vendorInformation.name)
# Fictional vendor GmbH

print(offers[0].vendorOffers[0].offers[0].price.amount)
# 10.99
# For Example if you use a valid sequence
```

At first we create a representation of the sequences we want to get offers for. We can start the search for these sequences by calling `pinger.searchOffers(sequences)`. 
It is designed that it can later be multithreaded or asynchronous. Thats why searchOffers has no return value.

With getOffers you can get the Offers. Take a look at `Pinger.py` and `Entities.py` to understand the structure of the return values.

The other functions and explainations are described in `Pinger.py`.