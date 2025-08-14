"""Config flow for Avanza Stock integration."""
from __future__ import annotations

import logging
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
                        vol.Optional(CONF_SHARES): float,
                        vol.Optional(CONF_PURCHASE_DATE): str,
                        vol.Optional(CONF_PURCHASE_PRICE): float,
                        vol.Optional(CONF_CONVERSION_CURRENCY): int,
                        vol.Optional(
                            CONF_INVERT_CONVERSION_CURRENCY, default=False
                        ): bool,
                        vol.Optional(
                            CONF_SHOW_TRENDING_ICON, default=DEFAULT_SHOW_TRENDING_ICON
                        ): bool,
                    }
                ),
            )

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

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SHARES,
                        default=self.config_entry.options.get(CONF_SHARES),
                    ): float,
                    vol.Optional(
                        CONF_PURCHASE_DATE,
                        default=self.config_entry.options.get(CONF_PURCHASE_DATE),
                    ): str,
                    vol.Optional(
                        CONF_PURCHASE_PRICE,
                        default=self.config_entry.options.get(CONF_PURCHASE_PRICE),
                    ): float,
                    vol.Optional(
                        CONF_CONVERSION_CURRENCY,
                        default=self.config_entry.options.get(CONF_CONVERSION_CURRENCY),
                    ): int,
                    vol.Optional(
                        CONF_INVERT_CONVERSION_CURRENCY,
                        default=self.config_entry.options.get(
                            CONF_INVERT_CONVERSION_CURRENCY, False
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_SHOW_TRENDING_ICON,
                        default=self.config_entry.options.get(
                            CONF_SHOW_TRENDING_ICON, DEFAULT_SHOW_TRENDING_ICON
                        ),
                    ): bool,
                }
            ),
        )
