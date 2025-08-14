"""Config flow for Avanza Stock integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_NAME

from .const import DOMAIN, DEFAULT_NAME, CONF_STOCK, CONF_SHARES, CONF_PURCHASE_DATE, CONF_PURCHASE_PRICE

_LOGGER = logging.getLogger(__name__)

class AvanzaStockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Avanza Stock."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the stock ID
                stock_id = user_input[CONF_STOCK]
                if not isinstance(stock_id, int) or stock_id <= 0:
                    errors["base"] = "invalid_stock_id"
                else:
                    # Check if this stock is already configured
                    await self.async_set_unique_id(str(stock_id))
                    self._abort_if_unique_id_configured()
                    
                    return self.async_create_entry(
                        title=user_input[CONF_NAME] or f"{DEFAULT_NAME} {stock_id}",
                        data=user_input
                    )
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_STOCK): int,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Optional(CONF_SHARES): vol.Coerce(float),
                vol.Optional(CONF_PURCHASE_DATE): str,
                vol.Optional(CONF_PURCHASE_PRICE): vol.Coerce(float),
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return AvanzaStockOptionsFlow(config_entry)


class AvanzaStockOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_SHARES, 
                    default=self.config_entry.data.get(CONF_SHARES)
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_PURCHASE_DATE, 
                    default=self.config_entry.data.get(CONF_PURCHASE_DATE)
                ): str,
                vol.Optional(
                    CONF_PURCHASE_PRICE, 
                    default=self.config_entry.data.get(CONF_PURCHASE_PRICE)
                ): vol.Coerce(float),
            })
        )
