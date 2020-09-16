# Generated by generate_tests (from the Hokohoko project).
import unittest as ut


class TestRun(ut.TestCase):
    def test_run_raises_an_error_if_period_is_None(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_raises_an_error_if_period_is_not_a_Period(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_raises_an_error_if_shared_config_is_None(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_raises_an_error_if_shared_config_is_not_a_HokohokoConfig(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_raises_an_error_if_config_is_None(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_raises_an_error_if_config_is_not_a_PeriodConfig(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_returns_an_account(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_the_account_contains_the_correct_amount_of_histories(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_run_the_history_is_correct_for_known_configurations(self):
        """Auto-generated from _run.py:49"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if_account_is_None(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if_account_is_not_an_Account(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if__locals_is_None(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if__locals_is_not_an_Account(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if_minute_is_None(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if_minute_is_not_a_list(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if_minute_is_empty(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_raises_an_error_if_minute_is_not_solely_Bars(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_correctly_closes_positions_if_they_closed_last_minute(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_correctly_opens_orders_if_they_opened_last_minute(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_correctly_closes_positions_if_they_closed_between_minutes(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_simulate_correctly_opens_orders_if_they_opened_between_minutes(self):
        """Auto-generated from _run.py:159"""
        self.fail('TODO: Implement me!')

    def test_open_position_raises_an_error_if_account_is_None(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_raises_an_error_if_account_is_not_an_Account(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_raises_an_error_if_position_id_is_None(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_raises_an_error_if_position_id_is_not_an_int(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_raises_an_error_if_position_id_is_less_than_0(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_raises_an_error_if__locals_is_None(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_raises_an_error_if__locals_is_not_a__Locals(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_moves_the_position_into_accountpositions(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_removes_the_position_from_accountpending(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_sets_the_pip_value_correctly(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_open_position_sets_the_pip_value_correctly_if_JPY(self):
        """Auto-generated from _run.py:318"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_account_is_None(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_account_is_not_an_Account(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_position_id_is_None(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_position_id_is_not_an_int(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_position_id_is_less_than_0(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_position_id_is_not_in_accountpositions(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_status_is_None(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if_status_is_not_a_Status(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if__locals_is_None(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_raises_an_error_if__locals_is_not_a__Locals(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_creates_a_History_in_accounthistory_for_this_position(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_removes_the_position_from_accountpositions(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_close_position_adjusts_accountbalance_correctly(self):
        """Auto-generated from _run.py:363"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_raises_an_error_if_requested_is_None(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_raises_an_error_if_requested_is_not_a_string(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_raises_an_error_if_available_is_None(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_raises_an_error_if_available_is_not_a_numpyndarray(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_returns_a_string(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_returns_symbols_which_are_their_own_base(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_returns_symbols_which_have_a_conversion_available(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_required_symbols_doesnt_return_symbols_which_have_no_conversion_available(self):
        """Auto-generated from _run.py:523"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_timestamps_is_None(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_timestamps_is_not_a_numpy_array(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_timestamps_is_empty(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_data_is_None(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_data_is_not_a_numpy_array(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_data_is_empty(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_graph_is_None(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_graph_is_empty(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_orders_are_None(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_orders_are_empty(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_orders_are_not_all_Orders(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_hold_minutes_is_negative(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_hold_minutes_is_0(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_timestamp_length_is_less_than_hold_minutes(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_raises_an_error_if_data_length_is_less_than_hold_minutes(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_returns_a_List_of_Results(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_returns_a_Result_for_every_position(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_calculate_positions_calculates_various_conditions_correctly(self):
        """Auto-generated from _run.py:565"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_raises_an_error_if_subset_ids_is_absent(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_raises_an_error_if_subset_ids_is_empty(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_raises_an_error_if_subset_ids_are_not_numpyint64s(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_raises_an_error_if_orders_does_not_contain_Orders_only(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_accepts_an_empty_orders_list(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_accepts_None_for_orders_list(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_returns_a_list_of_Orders(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_doesnt_remove_multiple_orders_per_symbol(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_removes_spurious_dont_orders(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_adds_all_missing_symbols_and_directions(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')

    def test_sanitize_orders_adds_missing_symbols_once_only(self):
        """Auto-generated from _run.py:640"""
        self.fail('TODO: Implement me!')


if __name__ == '__main__':
    ut.main()
