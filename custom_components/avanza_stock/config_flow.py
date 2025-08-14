"""Config flow for Avanza Stock integration."""
from __future__ import annotations

import logging
import re
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_CONVERSION_CURRENCY,
    CONF_INVERT_CONVERSION_CURRENCY,
    CONF_PURCHASE_DATE,
    CONF_PURCHASE_PRICE,
    CONF_SHARES,
    CONF_SHOW_TRENDING_ICON,
    CONF_STOCK,
    DEFAULT_NAME,
    DEFAULT_SHOW_TRENDING_ICON,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# Currency options for conversion
CURRENCY_OPTIONS = {
    "SEK": None,  # Default, no conversion
    "EUR": 18998,
    "USD": 19000,
    "GBP": 108703,
}

# Date validation regex
DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def validate_date_format(date_str: str) -> bool:
    """Validate date format YYYY-MM-DD."""
    if not date_str:
        return True  # Empty dates are allowed
    return bool(DATE_REGEX.match(date_str))


class AvanzaStockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Avanza Stock."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._data: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_STOCK): int,
                        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                        vol.Optional(CONF_SHARES): vol.All(
                            vol.Coerce(float),
                            vol.Range(min=0.000001, max=1000000)
                        ),
                        vol.Optional(CONF_PURCHASE_DATE): str,
                        vol.Optional(CONF_PURCHASE_PRICE): vol.All(
                            vol.Coerce(float),
                            vol.Range(min=0.000001, max=1000000)
                        ),
                        vol.Optional(CONF_CONVERSION_CURRENCY, default="SEK"): vol.In(
                            list(CURRENCY_OPTIONS.keys())
                        ),
                        vol.Optional(
                            CONF_INVERT_CONVERSION_CURRENCY, default=False
                        ): bool,
                        vol.Optional(
                            CONF_SHOW_TRENDING_ICON, default=DEFAULT_SHOW_TRENDING_ICON
                        ): bool,
                    }
                ),
            )

        # Validate the input
        errors = {}
        
        # Validate stock ID
        if user_input[CONF_STOCK] <= 0:
            errors["base"] = "invalid_stock_id"
        
        # Validate shares if provided
        if CONF_SHARES in user_input and user_input[CONF_SHARES] is not None:
            if user_input[CONF_SHARES] <= 0:
                errors["base"] = "invalid_shares"
        
        # Validate purchase price if provided
        if CONF_PURCHASE_PRICE in user_input and user_input[CONF_PURCHASE_PRICE] is not None:
            if user_input[CONF_PURCHASE_PRICE] <= 0:
                errors["base"] = "invalid_purchase_price"
        
        # Validate purchase date format if provided
        if CONF_PURCHASE_DATE in user_input and user_input[CONF_PURCHASE_DATE]:
            if not validate_date_format(user_input[CONF_PURCHASE_DATE]):
                errors["base"] = "invalid_date_format"
        
        if errors:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_STOCK, default=user_input[CONF_STOCK]): int,
                        vol.Optional(CONF_NAME, default=user_input.get(CONF_NAME, DEFAULT_NAME)): str,
                        vol.Optional(CONF_SHARES, default=user_input.get(CONF_SHARES)): vol.All(
                            vol.Coerce(float),
                            vol.Range(min=0.000001, max=1000000)
                        ),
                        vol.Optional(CONF_PURCHASE_DATE, default=user_input.get(CONF_PURCHASE_DATE)): str,
                        vol.Optional(CONF_PURCHASE_PRICE, default=user_input.get(CONF_PURCHASE_PRICE)): vol.All(
                            vol.Coerce(float),
                            vol.Range(min=0.000001, max=1000000)
                        ),
                        vol.Optional(CONF_CONVERSION_CURRENCY, default=user_input.get(CONF_CONVERSION_CURRENCY, "SEK")): vol.In(
                            list(CURRENCY_OPTIONS.keys())
                        ),
                        vol.Optional(
                            CONF_INVERT_CONVERSION_CURRENCY, default=user_input.get(CONF_INVERT_CONVERSION_CURRENCY, False)
                        ): bool,
                        vol.Optional(
                            CONF_SHOW_TRENDING_ICON, default=user_input.get(CONF_SHOW_TRENDING_ICON, DEFAULT_SHOW_TRENDING_ICON)
                        ): bool,
                    }
                ),
                errors=errors,
            )

        # Convert currency selection to actual ID for storage
        currency_selection = user_input.get(CONF_CONVERSION_CURRENCY, "SEK")
        user_input[CONF_CONVERSION_CURRENCY] = CURRENCY_OPTIONS[currency_selection]

        self._data = user_input
        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the confirmation step."""
        if user_input is None:
            stock_id = self._data[CONF_STOCK]
            name = self._data.get(CONF_NAME, f"{DEFAULT_NAME} {stock_id}")
            
            return self.async_show_form(
                step_id="confirm",
                description_placeholders={
                    "name": name,
                    "stock_id": str(stock_id),
                },
                data_schema=vol.Schema({}),
            )

        # Create the config entry
        title = self._data.get(CONF_NAME, f"{DEFAULT_NAME} {self._data[CONF_STOCK]}")

        return self.async_create_entry(
            title=title,
            data=self._data,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return AvanzaStockOptionsFlow(config_entry)


class AvanzaStockOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    def _get_currency_display_name(self, currency_id: int | None) -> str:
        """Convert currency ID back to display name for the options form."""
        if currency_id is None:
            return "SEK"
        for name, cid in CURRENCY_OPTIONS.items():
            if cid == currency_id:
                return name
        return "SEK"  # Default fallback

    def _get_default_value(self, key: str, fallback=None):
        """Get default value from options first, then from data, then fallback."""
        options_value = self.config_entry.options.get(key)
        data_value = self.config_entry.data.get(key)
        result = options_value if options_value is not None else data_value if data_value is not None else fallback
        
        _LOGGER.debug("Getting default value for %s: options=%s, data=%s, fallback=%s, result=%s", 
                      key, options_value, data_value, fallback, result)
        
        return result

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Validate the input
            errors = {}
            
            # Validate shares if provided
            if CONF_SHARES in user_input and user_input[CONF_SHARES] is not None:
                if user_input[CONF_SHARES] <= 0:
                    errors["base"] = "invalid_shares"
            
            # Validate purchase price if provided
            if CONF_PURCHASE_PRICE in user_input and user_input[CONF_PURCHASE_PRICE] is not None:
                if user_input[CONF_PURCHASE_PRICE] <= 0:
                    errors["base"] = "invalid_purchase_price"
            
            # Validate purchase date format if provided
            if CONF_PURCHASE_DATE in user_input and user_input[CONF_PURCHASE_DATE]:
                if not validate_date_format(user_input[CONF_PURCHASE_DATE]):
                    errors["base"] = "invalid_date_format"
            
            if errors:
                return self.async_show_form(
                    step_id="init",
                    data_schema=vol.Schema(
                        {
                            vol.Optional(
                                CONF_SHARES,
                                default=user_input.get(CONF_SHARES, self._get_default_value(CONF_SHARES)),
                            ): vol.All(
                                vol.Coerce(float),
                                vol.Range(min=0.000001, max=1000000)
                            ),
                            vol.Optional(
                                CONF_PURCHASE_DATE,
                                default=user_input.get(CONF_PURCHASE_DATE, self._get_default_value(CONF_PURCHASE_DATE)),
                            ): str,
                            vol.Optional(
                                CONF_PURCHASE_PRICE,
                                default=user_input.get(CONF_PURCHASE_PRICE, self._get_default_value(CONF_PURCHASE_PRICE)),
                            ): vol.All(
                                vol.Coerce(float),
                                vol.Range(min=0.000001, max=1000000)
                            ),
                            vol.Optional(
                                CONF_CONVERSION_CURRENCY,
                                default=user_input.get(CONF_CONVERSION_CURRENCY, self._get_currency_display_name(self._get_default_value(CONF_CONVERSION_CURRENCY))),
                            ): vol.In(
                                list(CURRENCY_OPTIONS.keys())
                            ),
                            vol.Optional(
                                CONF_INVERT_CONVERSION_CURRENCY,
                                default=user_input.get(
                                    CONF_INVERT_CONVERSION_CURRENCY, 
                                    self._get_default_value(CONF_INVERT_CONVERSION_CURRENCY, False)
                                ),
                            ): bool,
                            vol.Optional(
                                CONF_SHOW_TRENDING_ICON,
                                default=user_input.get(
                                    CONF_SHOW_TRENDING_ICON, 
                                    self._get_default_value(CONF_SHOW_TRENDING_ICON, DEFAULT_SHOW_TRENDING_ICON)
                                ),
                            ): bool,
                        }
                    ),
                    errors=errors,
                )
            
            # Convert currency selection to actual ID for storage
            currency_selection = user_input.get(CONF_CONVERSION_CURRENCY, "SEK")
            user_input[CONF_CONVERSION_CURRENCY] = CURRENCY_OPTIONS[currency_selection]
            
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SHARES,
                        default=self._get_default_value(CONF_SHARES),
                    ): vol.All(
                        vol.Coerce(float),
                        vol.Range(min=0.000001, max=1000000)
                    ),
                    vol.Optional(
                        CONF_PURCHASE_DATE,
                        default=self._get_default_value(CONF_PURCHASE_DATE),
                    ): str,
                    vol.Optional(
                        CONF_PURCHASE_PRICE,
                        default=self._get_default_value(CONF_PURCHASE_PRICE),
                    ): vol.All(
                        vol.Coerce(float),
                        vol.Range(min=0.000001, max=1000000)
                    ),
                    vol.Optional(
                        CONF_CONVERSION_CURRENCY,
                        default=self._get_currency_display_name(self._get_default_value(CONF_CONVERSION_CURRENCY)),
                    ): vol.In(
                        list(CURRENCY_OPTIONS.keys())
                    ),
                    vol.Optional(
                        CONF_INVERT_CONVERSION_CURRENCY,
                        default=self._get_default_value(
                            CONF_INVERT_CONVERSION_CURRENCY, False
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_SHOW_TRENDING_ICON,
                        default=self._get_default_value(
                            CONF_SHOW_TRENDING_ICON, DEFAULT_SHOW_TRENDING_ICON
                        ),
                    ): bool,
                }
            ),
        )
