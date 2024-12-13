#!/usr/bin/env python3

from django.core.management.base import BaseCommand

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_altaviz.settings')
django.setup()

from app_bank.models import State, Bank
from app_users.models import Region, User
from app_fault.models import FaultName
from app_location.models import Location

regionAndStateList = {
	'north': [
		'taraba:TA', 'yobe:YO', 'zamfara:ZA', 'abuja:FC', 'kaduna:KD',
		'sokoto:SO', 'bauchi:BA', 'adamawa:AD', 'benue:BE', 'borno:BO',
		'gombe:GO', 'jigawa:JI', 'kano:KN', 'katsina:KT', 'kebbi:KE',
		'kogi:KO', 'kwara:KW', 'nassarawa:NA', 'niger:NI', 'plateau:PL'
	],
	'west': [
		'lagos:LA', 'ogun:OG', 'osun:OS', 'ekiti:EK', 'ondo:ON', 'oyo:OY'
	],
	'south': [
		'enugu:EN', 'bayelsa:BY', 'ebonyi:EB', 'abia:AB', 'akwa ibom:AK',
		'anambra:AN', 'cross river:CR', 'delta:DE', 'edo:ED', 'imo:IM',
		'rivers:RI'
	]
}
faultNameList = [
	'Blank Screen', 'Cash Jam', 'Card Not Smart',
	'Poor Facial Image', 'Unable to Clear/Load Cash',
	'ATM not Dispensing notes', 'Reject Bin Full',
	'Dispenser not Spinning',
	'Dispenser spins too many times without paying',
	'ATM/Dispenser dirty'
]

# Create a management command class extending BaseCommand
class Command(BaseCommand):  # added class definition to use Django management command system
	help = 'Creates initial regions, states, banks, faults, locations, and admin user'
	def handle(self, *args, **kwargs):
		print('initiating ...')

		print()
		# create regions
		print('checking/creating regions ...')
		if not Region.objects.exists():
			for neweRegion in regionAndStateList.keys():
				reg = Region.objects.create(name=neweRegion)
				print(f'created: {reg} ...')

		west = Region.objects.get(name='west')
		print(f'got the region: {west}')

		print()
		# create states
		print('checking/creating states ...')
		if not State.objects.exists():
			for region, states in regionAndStateList.items():
				region_obj = Region.objects.get(name=region)
				for state in states:
					name, initial = state.split(':')
					st = State.objects.create(
						name=name, initial=initial,
						region=region_obj
					)
					print(f'created: {st} ...')

		lagos = State.objects.get(name='lagos')
		print(f'got the state: {lagos}')

		print()
		# create bank
		print('checking/creating bank ...')
		if not Bank.objects.exists():
			bank = Bank.objects.create(name='fcmb')
			bank.states.add(lagos)
			print(f'created: {bank} ...')

		fcmb = Bank.objects.get(name='fcmb')
		print(f'got the bank: {fcmb}')

		print()
		# create fault names
		print('checking/creating fault names ...')
		if not FaultName.objects.exists():
			for faultName in faultNameList:
				fname = FaultName.objects.create(name=faultName)
				print(f'created: {fname} ...')

		print()
		# create location
		print('checking/creating location ...')
		if not Location.objects.exists():
			location = Location.objects.create(
				location='ajah',
				state=lagos,
				region=west
			)
			location.bank.add(fcmb)
			print(f'created: {location} ...')

		ajah = Location.objects.get(location='ajah')
		print(f'got the location: {ajah}')

		print()
		# create admin user
		adminUser = User.objects.create_superuser(
			email='ogagadafetite@gmail.com',
			username='dafetite', password='debbydafe',
			first_name='dafetite', last_name='ogaga',
			middle_name='otegbeye', phone='08038091572',
			wphone='08038091572',
			address='12 abak crescent, addo, ajah',
			gender='male', role='human-resource',
			aboutme='the app developer',
			location=ajah, state=lagos, region=west
		)

		print(f'Admin user ({adminUser.first_name}) created successfully')
